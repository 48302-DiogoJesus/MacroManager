export function replaceMacroInterval(sourceCode: string, newInterval: string): string {
    // Define a regular expression pattern to match @Macro decorator with optional arguments
    const macroRegex = /@Macro\(([^)]*)\)/;

    // Replace the interval value in the @Macro decorator while preserving other arguments
    const modifiedCode = sourceCode.replace(macroRegex, (match, args) => {
        const argsArray = args.split(',').map(arg => {
            if (arg.trim().startsWith('interval_s=')) {
                return `interval_s=${newInterval}`;
            }
            return arg.trim();
        });
        return `@Macro(${argsArray.join(', ')})`;
    });

    return modifiedCode;
}