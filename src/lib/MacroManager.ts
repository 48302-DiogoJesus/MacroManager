import type { IMacroManager } from './IMacroManager';
import type { Folder } from './FileSystemTree';
import type { IMacro } from './IMacro';
import os from "os";
import { getLatestMacroLogs, getMacrosFlat } from './FileSystemUtils';
import { exec } from "child_process"
import path from 'path';
import fs from 'fs-extra';
import { macroBoilerplate } from './macro-boilerplate';

const MacrosPath = os.userInfo().homedir + '\\MacroManager';
const DEFAULT_MACRO_NAME = "macro.py"

export const MacroManager: IMacroManager = {
    // Returns the full path of the macro
    createMacro: function (macro_name: string): string {
        const folderFullPath = path.join(MacrosPath, macro_name);
        const pythonFilePath = path.join(folderFullPath, DEFAULT_MACRO_NAME);

        // Create the folder
        fs.mkdirSync(folderFullPath);

        // Create file with boilerplate
        fs.writeFileSync(pythonFilePath, macroBoilerplate);

        return pythonFilePath;
    },

    openMacrosFolder: () => exec(`explorer "${MacrosPath}"`),
    openMacroInCodeEditor: (absoluteMacroPath: string) => exec(`code "${absoluteMacroPath}"`),
    openMacroInFileExplorer: (absoluteMacroPath: string) => exec(`explorer "${path.dirname(absoluteMacroPath)}"`),
    openTaskScheduler: () => exec(`taskschd.msc`),

    getMacrosFlat: () => getMacrosFlat(MacrosPath),

    getMacrosFolderTreeLike: function (): Promise<Folder> {
        throw new Error('Implement Later');
    },

    getLatestMacroLogs: getLatestMacroLogs,

    runMacro: (absoluteMacroPath: string) => exec(`pythonw "${absoluteMacroPath}"`),

    shouldUpdateFramework: function (): Promise<boolean> {
        throw new Error('Function not implemented.');
    },
    shouldUpdateManager: function (): Promise<boolean> {
        throw new Error('Function not implemented.');
    },

    updateFramework: function (): Promise<void> {
        throw new Error('Function not implemented.');
    },
    updateManager: function (): Promise<void> {
        throw new Error('Function not implemented.');
    }
}