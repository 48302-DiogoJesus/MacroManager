<script lang="ts">
  import type {
    InvocationVariableDetails,
    InvocationVariableName,
  } from '$lib/IMacroManager';
  import { executeRPC } from '$lib/client/executeRPC';
  import Button from '$lib/components/ui/button/button.svelte';
  import { Input } from '$lib/components/ui/input';
  import Label from '$lib/components/ui/label/label.svelte';
  import * as Select from '$lib/components/ui/select';
  import Separator from '$lib/components/ui/separator/separator.svelte';
  import { onMount } from 'svelte';

  export let macroPath: string;

  const clearErrorTimeS = 5;
  let errorInterval;
  let errorMessage: string | null = null;

  let invocationVariables:
    | 'loading'
    | null
    | {
        [key: InvocationVariableName]: InvocationVariableDetails;
      } = 'loading';

  let invocationVariablesValues: { [key: InvocationVariableName]: string } = {};

  function getInvocationVariablesMD(): Promise<null | {
    [key: InvocationVariableName]: InvocationVariableDetails;
  }> {
    return new Promise((res) => {
      executeRPC('getMacroInvocationVariablesMetadata', [macroPath], (data) => {
        res(Object.keys(data).length == 0 ? null : data);
      });
    });
  }

  function runMacro() {
    if (invocationVariables == 'loading' || invocationVariables == null) return;

    if (errorInterval) clearInterval(errorInterval);
    errorMessage = null;

    if (
      Object.keys(invocationVariablesValues).length !=
      Object.keys(invocationVariables).length
    ) {
      errorMessage =
        'Some variables are missing. You need to provide a value for all the variables';

      errorInterval = setTimeout(
        () => (errorMessage = null),
        clearErrorTimeS * 1000
      );
      return;
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
      errorMessage = typeErrorsMsgs.join('; ');
      errorInterval = setTimeout(
        () => (errorMessage = null),
        clearErrorTimeS * 1000
      );
      return;
    }

    executeRPC('runMacro', [macroPath, invocationVariablesValues]);
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
    <Input value="1" class="w-28" type="number" />
    seconds
  </span>

  {#if invocationVariables == 'loading'}
    <p>Loading...</p>
  {:else if invocationVariables != null}
    {#if invocationVariables}
      <Label class="mb-3 text-lg underline underline-offset-4"
        >Invocation Variables</Label
      >

      <div
        id="invocation-variables"
        class="flex flex-col gap-3 max-h-[80vh] overflow-y-auto"
      >
        {#each Object.entries(invocationVariables) as [varname, { type, accepted_values }]}
          <div class="flex items-center gap-3 variable">
            <div class="flex items-center gap-1 border-1">
              <span />
              {varname} <code> ({type})</code>
            </div>

            {#if accepted_values}
              <Select.Root portal={null}>
                <Select.Trigger class="border-2">
                  <Select.Value placeholder="Select a value" />
                </Select.Trigger>
                <Select.Content>
                  <Select.Group>
                    {#each accepted_values as accepted_value}
                      <Select.Item
                        on:click={() => {
                          invocationVariablesValues[varname] = accepted_value;
                        }}
                        class="py-2"
                        value={accepted_value}
                        label={accepted_value}>{accepted_value}</Select.Item
                      >
                    {/each}
                  </Select.Group>
                </Select.Content>
                <Select.Input name="favoriteFruit" />
              </Select.Root>
            {:else}
              <Input
                class="border-2"
                on:input={(e) => {
                  invocationVariablesValues[varname] = e.currentTarget.value;
                }}
              />
            {/if}
            <br />
          </div>
        {/each}
      </div>
    {/if}
  {/if}

  <br />

  <Button
    class="bg-green-600 hover:bg-green-500 text-slate-200"
    on:click={runMacro}
  >
    Run
  </Button>
</div>
