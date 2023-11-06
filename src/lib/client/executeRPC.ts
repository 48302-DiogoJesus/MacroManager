import type { IMacroManager } from "$lib/IMacroManager";

export type ErrorMessage = string

export async function executeRPC<K extends keyof IMacroManager>(
    rpcName: K,
    args: Parameters<IMacroManager[K]>,
    onSuccess?: (data: Awaited<ReturnType<IMacroManager[K]>>) => void,
    onError?: (error_msg: string) => void
): Promise<void> {
    const res = await fetch('/api', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            fn: rpcName,
            args: args,
        }),
    })

    const jsonBody = await res.json()

    if (jsonBody.error) {
        (window as any).message("Error", jsonBody.error_msg, 7)
        onError?.(jsonBody.error_msg)
    } else {
        onSuccess?.(jsonBody.data)
    }
}