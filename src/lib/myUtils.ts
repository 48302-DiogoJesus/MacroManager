import type { InvocationVariableDetails, InvocationVariableName } from "./IMacroManager";

export function validateMacroRPC(
    macroPath: string,
    invocationVariables: { [key: InvocationVariableName]: InvocationVariableDetails },
    invocationVariablesValues: { [key: InvocationVariableName]: string },
    timeBetweenInstructionsS: string
): "valid" | Error {
    if (isNaN(parseFloat(timeBetweenInstructionsS))) {
        return Error(`Invalid time between instructions: ${timeBetweenInstructionsS}`)
    }
    if (
        Object.keys(invocationVariablesValues).length !=
        Object.keys(invocationVariables).length
    ) {
        return Error('Some variables are missing. You need to provide a value for all the variables')
    }

    const typeErrorsMsgs = [];
    for (const [varname, value] of Object.entries(invocationVariablesValues)) {
        const { type, accepted_values } = invocationVariables[varname];

        if (accepted_values != null) continue; // these should be autocomplete making it imposible to have invalid value

        if (type == 'number') {
            if (value.includes(' ') || isNaN(parseFloat(value))) {
                typeErrorsMsgs.push(`${varname} must be a number`);
            }
        }
    }
    if (typeErrorsMsgs.length > 0) {
        return Error(typeErrorsMsgs.join('; '))
    }

    return "valid"
}