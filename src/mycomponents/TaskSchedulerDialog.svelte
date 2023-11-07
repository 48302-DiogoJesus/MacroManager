<script lang="ts">
  import * as Dialog from '$lib/components/ui/dialog';
  import { Button } from '$lib/components/ui/button';
  import FaClipboardCheck from 'svelte-icons/fa/FaClipboardCheck.svelte';
  import FaRegClipboard from 'svelte-icons/fa/FaRegClipboard.svelte';
  import { executeRPC } from '$lib/client/executeRPC';

  export let macroPath: string;

  const command = `pythonw ${macroPath}`;
  let copiedToClipboard = false;

  function copyToClipboard() {
    if (copiedToClipboard) return;

    navigator.clipboard.writeText(command);
    copiedToClipboard = true;
    setTimeout(() => (copiedToClipboard = false), 2000);
  }
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
    <div class="flex flex-col items-center justify-center gap-8 mt-4">
      <div class="flex items-center justify-start gap-5">
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
