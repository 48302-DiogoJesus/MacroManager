<script lang="ts">
  import * as Dialog from '$lib/components/ui/dialog';
  import { Button } from '$lib/components/ui/button';
  import FaClipboardCheck from 'svelte-icons/fa/FaClipboardCheck.svelte';
  import FaRegClipboard from 'svelte-icons/fa/FaRegClipboard.svelte';
  import { executeRPC } from '$lib/client/executeRPC';
  import type {
    InvocationVariableName,
    InvocationVariableDetails,
  } from '$lib/types/IMacroManager';
  import { onMount } from 'svelte';
  import { validateMacroRPC } from '$lib/utils/myUtils';
  import InvocationVariablesForm from './InvocationVariablesForm.svelte';
  import Label from '$lib/components/ui/label/label.svelte';
  import { Input } from '$lib/components/ui/input';

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

  let invocationVariablesValues: { [key: InvocationVariableName]: string } = {};
  let timeBetweenInstructionsS: string = '1';

  const baseCommand = `pythonw ${macroPath}`;
  let command = baseCommand + ` --interval_s=${timeBetweenInstructionsS}`;
  let copiedToClipboard = false;

  $: {
    timeBetweenInstructionsS;

    updateCommand();
  }

  function showError(message: string) {
    errorMessage = message;

    errorInterval = setTimeout(
      () => (errorMessage = null),
      clearErrorTimeS * 1000
    );
  }

  function getInvocationVariablesMD(): Promise<null | {
    [key: InvocationVariableName]: InvocationVariableDetails;
  }> {
    return new Promise((res) => {
      executeRPC('getMacroInvocationVariablesMetadata', [macroPath], (data) => {
        res(Object.keys(data).length == 0 ? null : data);
      });
    });
  }

  function updateCommand() {
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
    } else {
      // Reset to base command
      command = baseCommand;
      // Append invocation variables
      for (const [key, value] of Object.entries(invocationVariablesValues)) {
        command += ` ${key}="${value}"`;
      }
      if (timeBetweenInstructionsS) {
        command += ` --interval_s=${timeBetweenInstructionsS}`;
      }
    }
  }

  function copyToClipboard() {
    if (copiedToClipboard) return;

    navigator.clipboard.writeText(command);
    copiedToClipboard = true;
    setTimeout(() => (copiedToClipboard = false), 2000);
  }

  onMount(async () => (invocationVariables = await getInvocationVariablesMD()));
</script>

<Dialog.Root closeOnOutsideClick={false} closeOnEscape={false}>
  <Dialog.Trigger>
    <slot />
  </Dialog.Trigger>
  <Dialog.DialogContent class="min-w-[50vw]">
    <Dialog.Header>
      <Dialog.Title class="text-2xl">Schedule Macro</Dialog.Title>
      <Dialog.Description>Using Windows Task Scheduler</Dialog.Description>
    </Dialog.Header>
    <div class="flex flex-col gap-3 mt-2 max-h-[80vh]">
      {#if errorMessage}
        <p class="text-lg font-bold text-red-600">ERROR: {errorMessage}</p>
      {/if}

      <Label class="text-lg underline underline-offset-4"
        >Interval Between Operations</Label
      >
      <span class="flex items-center gap-3 mb-3">
        <Input
          value="1"
          class="w-28"
          type="number"
          on:input={(e) => {
            const newInterval = e.currentTarget.value;
            if (newInterval) timeBetweenInstructionsS = e.currentTarget.value;
          }}
        />
        seconds
      </span>

      <InvocationVariablesForm
        onChange={updateCommand}
        {invocationVariables}
        {invocationVariablesValues}
      />

      <Label class="mb-3 text-lg underline underline-offset-4">
        Final Command
      </Label>

      <div class="flex items-center justify-start gap-3 mb-4">
        <!-- svelte-ignore a11y-click-events-have-key-events -->
        <!-- svelte-ignore a11y-no-static-element-interactions -->
        <button class="icon text-slate-300" on:click={copyToClipboard}>
          {#if copiedToClipboard}
            <FaClipboardCheck />
          {:else}
            <FaRegClipboard />
          {/if}
        </button>
        <code>{command}</code>
      </div>

      <Button on:click={() => executeRPC('openTaskScheduler', [])}
        >Open Task Scheduler</Button
      >
    </div>
  </Dialog.DialogContent>
</Dialog.Root>
