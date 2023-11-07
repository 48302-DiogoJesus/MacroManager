import type { Folder } from "./FileSystemTree"
import type { IMacro } from "./IMacro"

export interface IMacroManager {
    // Creates a template macro.py inside macros folder %userprofile%/MacroManager
    createMacro(name: string): string

    // Opens macros folder %userprofile%/MacroManager
    openMacrosFolder(): void
    openMacroInCodeEditor(absoluteMacroPath: string): void
    openMacroInFileExplorer(absoluteMacroPath: string): void
    openTaskScheduler(): void

    getMacrosFlat(): Promise<Array<IMacro>>

    getMacrosFolderTreeLike(): Promise<Folder>

    getLatestMacroLogs(absoluteMacroPath: string): Promise<Array<string>>,

    runMacro(
        absoluteMacroPath: string,
        invocationVariables: { [key: InvocationVariableName]: InvocationVariableValue },
        timeBetweenInstructionsS?: string
    ): void

    getMacroInvocationVariablesMetadata(absoluteMacroPath: string): { [key: InvocationVariableName]: InvocationVariableDetails }

    getFrameworkVersions(): Promise<{
        shouldUpdate: boolean
        currentVersion: string
        remoteVersion: string
    }>

    shouldUpdateManager(): Promise<boolean>

    updateFramework(): Promise<void>
    updateManager(): Promise<void>
}

export type InvocationVariableName = string
export type InvocationVariableDetails = { type: "string" | "number", accepted_values: Array<string> | null }
export type InvocationVariableValue = string