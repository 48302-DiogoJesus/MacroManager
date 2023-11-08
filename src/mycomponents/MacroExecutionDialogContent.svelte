<script lang="ts">
  import type {
    InvocationVariableDetails,
    InvocationVariableName,
  } from '$lib/types/IMacroManager';
  import { executeRPC } from '$lib/client/executeRPC';
  import Button from '$lib/components/ui/button/button.svelte';
  import { Input } from '$lib/components/ui/input';
  import Label from '$lib/components/ui/label/label.svelte';
  import * as Select from '$lib/components/ui/select';
  import Separator from '$lib/components/ui/separator/separator.svelte';
  import { validateMacroRPC } from '$lib/utils/myUtils';
  import { onMount } from 'svelte';
  import InvocationVariablesForm from './InvocationVariablesForm.svelte';

  export let macroPath: string;

  const clearErrorTimeS = 5;
  let errorInterval: any;
  let errorMessage: string | null = null;

  let invocationVariables:
    | 'loading'
    | null
    | {
        [key: InvocationVariableName]: InvocationVariableDetails;
      } = 'loading';

  let invocationVariablesValues: {
    [key: InvocationVariableName]: string;
  } = {};
  let timeBetweenInstructionsS: string = '1';

  function getInvocationVariablesMD(): Promise<null | {
    [key: InvocationVariableName]: InvocationVariableDetails;
  }> {
    return new Promise((res) =>
      executeRPC('getMacroInvocationVariablesMetadata', [macroPath], (data) => {
        res(Object.keys(data).length == 0 ? null : data);
      })
    );
  }

  function showError(message: string) {
    errorMessage = message;

    errorInterval = setTimeout(
      () => (errorMessage = null),
      clearErrorTimeS * 1000
    );
  }

  function runMacro() {
    if (invocationVariables == 'loading') return;

    if (errorInterval) clearInterval(errorInterval);
    errorMessage = null;

    const result = validateMacroRPC(
      macroPath,
      invocationVariables,
      invocationVariablesValues,
      timeBetweenInstructionsS
    );

    if (result != 'valid') {
      showError(result.message);
      return;
    }

    executeRPC('runMacro', [
      macroPath,
      invocationVariablesValues,
      timeBetweenInstructionsS,
    ]);
  }

  onMount(async () => (invocationVariables = await getInvocationVariablesMD()));
</script>

<div class="flex flex-col gap-1 pt-4">
  {#if errorMessage}
    <p class="mb-6 text-lg font-bold text-red-600">ERROR: {errorMessage}</p>
  {/if}

  <Label class="mb-3 text-lg underline underline-offset-4"
    >Interval Between Operations</Label
  >
  <span class="flex items-center gap-3 mb-3">
    <Input
      value="1"
      class="w-28"
      type="number"
      on:input={(e) => (timeBetweenInstructionsS = e.currentTarget.value)}
    />
    seconds
  </span>

  <InvocationVariablesForm {invocationVariables} {invocationVariablesValues} />

  <br />

  <Button
    class="bg-green-600 hover:bg-green-500 text-slate-200"
    on:click={runMacro}
  >
    Run
  </Button>
</div>
