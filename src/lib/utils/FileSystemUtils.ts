import fs from 'fs-extra';
import path from 'path';
import type { IMacro } from '../types/IMacro';
import { templateMacroPath } from '$lib/MacroManager';

export async function getMacrosFlat(root_dir: string): Promise<Array<IMacro>> {
    try {
        const fileList: Array<IMacro> = [];

        async function search(directory: string) {
            const files = await fs.readdir(directory);

            for (const file of files) {
                const filePath = path.join(directory, file);
                const stats = await fs.stat(filePath);

                if (stats.isDirectory()) {
                    // Recursively search subdirectories
                    await search(filePath);
                } else if (stats.isFile() && path.extname(filePath) === '.py') {
                    const fileContents = await fs.readFile(filePath, 'utf8');
                    if (fileContents.includes('@Macro')) {
                        const folderName = path.basename(directory);
                        const logsPath = path.join(directory, 'logs');

                        let lastRunDate = undefined;

                        if (await fs.pathExists(logsPath)) {
                            const logFiles = await fs.readdir(logsPath);
                            if (logFiles.length > 0) {
                                logFiles.sort((a, b) => {
                                    // Extract date and time components from file names
                                    const dateA = a.split(' ')[0];
                                    const timeA = a.split(' ')[1].replace(/\./g, ':');
                                    const dateB = b.split(' ')[0];
                                    const timeB = b.split(' ')[1].replace(/\./g, ':');

                                    // Create Date objects for date and time
                                    const dateObjA = new Date(dateA + 'T' + timeA);
                                    const dateObjB = new Date(dateB + 'T' + timeB);

                                    // Reverse the comparison to sort most recent files first
                                    return dateObjB.getTime() - dateObjA.getTime();
                                });

                                const dateTimePart = logFiles.pop().replace('.txt', '');
                                const [datePart, timePart] = dateTimePart.split(' '); // Split by space

                                // Extract the year, month, day, hour, minute, and second
                                const [year, month, day] = datePart.split('-');
                                const [hour, minute, second] = timePart.split('.');

                                lastRunDate = new Date(Number(year), Number(month) - 1, Number(day), Number(hour), Number(minute), Number(second));
                            }
                        }

                        fileList.push({ name: folderName, path: filePath, last_run: lastRunDate });
                    }
                }
            }
        }

        await search(root_dir);
        return fileList.filter(file => file.path != templateMacroPath);
    } catch (error) {
        console.error('Error searching Python files:', error);
        return [];
    }
}

export async function getLatestMacroLogs(absoluteMacroPath: string): Promise<Array<string>> {
    const logsFolder = path.join(path.dirname(absoluteMacroPath), "logs")

    if (!fs.existsSync(logsFolder))
        throw Error("Could not find logs folder at " + logsFolder)

    const logFiles = await fs.readdir(logsFolder);

    if (logFiles.length == 0)
        throw Error("Could not find logs folder at " + logsFolder)

    logFiles.sort((a, b) => {
        // Extract date and time components from file names
        const dateA = a.split(' ')[0];
        const timeA = a.split(' ')[1].replace(/\./g, ':');
        const dateB = b.split(' ')[0];
        const timeB = b.split(' ')[1].replace(/\./g, ':');

        // Create Date objects for date and time
        const dateObjA = new Date(dateA + 'T' + timeA);
        const dateObjB = new Date(dateB + 'T' + timeB);

        // Reverse the comparison to sort most recent files first
        return dateObjB.getTime() - dateObjA.getTime();
    });

    const latestLogFile = path.join(logsFolder, logFiles.pop());

    const logContents = fs.readFileSync(latestLogFile, { encoding: "utf-8" })

    return logContents.split("\n")
}