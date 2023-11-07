import type { RequestHandler } from './$types';
import { MacroManager } from '$lib/MacroManager';

type RPC = {
    fn: string
    args: any[]
}

export const POST: RequestHandler = async ({ request, url }) => {
    const { fn, args }: RPC = await request.json()

    console.log("RPC call", fn, args)

    try {
        const result = await MacroManager[fn](...args)
        // console.log("RPC complete", result)
        return Response.json({ error: false, data: result });
    } catch (ex) {
        // console.log("RPC error:", ex.message)
        return Response.json({ error: true, error_msg: ex.message });
    }
};