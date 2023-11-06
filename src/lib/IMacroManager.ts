import type { Folder } from "./FileSystemTree"
import type { IMacro } from "./IMacro"

export interface IMacroManager {
    // Creates a boilerplate macro.py inside macros folder %userprofile%/MacroManager
    createMacro(name: string): string

    // Opens macros folder %userprofile%/MacroManager
    openMacrosFolder(): void
    openMacroInCodeEditor(absoluteMacroPath: string): void
    openMacroInFileExplorer(absoluteMacroPath: string): void
    openTaskScheduler(): void

    getMacrosFlat(): Promise<Array<IMacro>>

    getMacrosFolderTreeLike(): Promise<Folder>

    getLatestMacroLogs(absoluteMacroPath: string): Promise<Array<string>>,

    runMacro(absoluteMacroPath: string): void

    shouldUpdateFramework(): Promise<boolean>
    shouldUpdateManager(): Promise<boolean>

    updateFramework(): Promise<void>
    updateManager(): Promise<void>
} 