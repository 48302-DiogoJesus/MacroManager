<script lang="ts">
  import type { IMacroManager } from './../lib/IMacroManager';
  import TooltipWrapper from './../mycomponents/TooltipWrapper.svelte';
  import * as Table from '$lib/components/ui/table';
  import * as Tooltip from '$lib/components/ui/tooltip';
  import { Loader2 } from 'lucide-svelte';
  import { Button } from '$lib/components/ui/button';
  import * as Dialog from '$lib/components/ui/dialog';
  import { Input } from '$lib/components/ui/input';
  import { Separator } from '$lib/components/ui/separator';

  import FaPlus from 'svelte-icons/fa/FaPlus.svelte';
  import FaPlay from 'svelte-icons/fa/FaPlay.svelte';
  import MdFolder from 'svelte-icons/md/MdFolder.svelte';
  import FaCode from 'svelte-icons/fa/FaCode.svelte';
  import FaFileAlt from 'svelte-icons/fa/FaFileAlt.svelte';
  import FaClock from 'svelte-icons/fa/FaClock.svelte';
  import FaRedo from 'svelte-icons/fa/FaRedo.svelte';
  import FaRegClipboard from 'svelte-icons/fa/FaRegClipboard.svelte';
  import TaskSchedulerDialog from '../mycomponents/TaskSchedulerDialog.svelte';
  import { onMount } from 'svelte';
  import { executeRPC } from '$lib/client/executeRPC';
  import DialogContent from '$lib/components/ui/dialog/dialog-content.svelte';
  import Label from '$lib/components/ui/label/label.svelte';
  import TaskCreatorDialog from '../mycomponents/TaskCreatorDialog.svelte';

  let isRefreshing = false;
  let macros: Awaited<ReturnType<IMacroManager['getMacrosFlat']>> = [];

  let filterText: string | null = null;
  $: macrosFiltered = filterText
    ? macros.filter(
        (m) =>
          m.name.toLowerCase().includes(filterText.toLowerCase()) ||
          m.path.toLowerCase().includes(filterText.toLowerCase()) ||
          m.last_run
            .toUTCString()
            .toLowerCase()
            .includes(filterText.toLowerCase())
      )
    : null;

  async function executeLogsRPC(
    absoluteMacroPath: string
  ): Promise<Array<string>> {
    return new Promise((res) =>
      executeRPC('getLatestMacroLogs', [absoluteMacroPath], res)
    );
  }

  async function refreshFlatMacroList() {
    if (isRefreshing) return;
    isRefreshing = true;

    await executeRPC('getMacrosFlat', [], (result) => {
      macros = result.map((macro) => ({
        ...macro,
        last_run: !macro.last_run ? undefined : new Date(macro.last_run),
      }));
    });

    isRefreshing = false;
  }

  onMount(() => {
    refreshFlatMacroList();
  });
</script>

<h1 class="ml-0">Macro Manager</h1>

<p class="my-6 text-lg text-slate-200">
  Manages your macros located at <code>%userprofile%\MacroManager</code>
</p>

<div id="buttons" class="flex items-center justify-start gap-3">
  <TaskCreatorDialog refreshList={refreshFlatMacroList}>
    <Button variant="secondary" class="bg-green-600 hover:bg-green-500">
      <span class="mr-3 icon">
        <FaPlus />
      </span>
      New
    </Button>
  </TaskCreatorDialog>

  <Button
    variant="secondary"
    class="my-4 bg-blue-800 hover:bg-blue-700"
    disabled={isRefreshing}
    on:click={refreshFlatMacroList}
  >
    <span class="mr-3 icon">
      <FaRedo />
    </span>
    {isRefreshing ? 'Refreshing' : 'Refresh'}
  </Button>

  <Button
    variant="secondary"
    class="my-4 bg-yellow-700 hover:bg-yellow-600"
    on:click={() => executeRPC('openMacrosFolder', [])}
  >
    <span class="mr-3 icon">
      <MdFolder />
    </span>
    Open Macros Folder
  </Button>
</div>

<Input
  class="max-w-sm my-3 border-[3px]"
  placeholder="Filter by name, path or last run ..."
  type="text"
  bind:value={filterText}
/>

<div class="border-2 rounded-md">
  <Table.Root>
    <Table.Header>
      <Table.Row>
        <Table.Head />
        <Table.Head>Name</Table.Head>
        <Table.Head>Path</Table.Head>
        <Table.Head>Last Run</Table.Head>
      </Table.Row>
    </Table.Header>
    <Table.Body>
      {#each macrosFiltered || macros as macro}
        <Table.Row>
          <Table.Cell>
            <!-- svelte-ignore a11y-no-static-element-interactions -->
            <TooltipWrapper msg="Run Macro">
              <!-- svelte-ignore a11y-click-events-have-key-events -->
              <span
                class="text-green-500 icon"
                on:click={() => executeRPC('runMacro', [macro.path])}
              >
                <FaPlay />
              </span>
            </TooltipWrapper>
          </Table.Cell>

          <Table.Cell class="text-lg font-bold text-slate-300"
            >{macro.name}</Table.Cell
          >
          <Table.Cell class="text-sm">{macro.path}</Table.Cell>
          <Table.Cell class="flex items-center justify-start gap-4">
            {macro.last_run ? macro.last_run.toUTCString() : 'N/A'}
            <Dialog.Root>
              <Dialog.Trigger>
                <!-- svelte-ignore a11y-click-events-have-key-events -->
                <TooltipWrapper msg="See Last Run Logs">
                  <!-- svelte-ignore a11y-click-events-have-key-events -->
                  <!-- svelte-ignore a11y-no-static-element-interactions -->
                  <span class="text-slate-300 icon">
                    <FaFileAlt />
                  </span>
                </TooltipWrapper>
              </Dialog.Trigger>
              <Dialog.DialogContent class="min-w-[90vw] pt-14">
                <div id="logs" class="overflow-auto max-h-[80vh]">
                  {#await executeLogsRPC(macro.path)}
                    <p>Loading Logs for {macro.path}...</p>
                  {:then log_lines}
                    {#each log_lines as log_line, idx}
                      {#if idx < log_lines.length}
                        <Separator
                          class="my-1 border-2"
                          orientation="horizontal"
                        />
                      {/if}
                      <div class="w-[90%] py-1">
                        {log_line}
                      </div>
                    {/each}
                  {:catch}
                    <p>
                      Could not load Logs for {macro.path}! Try to go to the
                      Logs folder manually
                    </p>
                  {/await}
                </div>
              </Dialog.DialogContent>
            </Dialog.Root>
          </Table.Cell>

          <Table.Cell>
            <!-- svelte-ignore a11y-no-static-element-interactions -->
            <TooltipWrapper msg="Open in File Explorer">
              <!-- svelte-ignore a11y-click-events-have-key-events -->
              <span
                class="text-yellow-300 icon"
                on:click={() =>
                  executeRPC('openMacroInFileExplorer', [macro.path])}
              >
                <MdFolder />
              </span>
            </TooltipWrapper>
          </Table.Cell>

          <Table.Cell>
            <!-- svelte-ignore a11y-click-events-have-key-events -->
            <TooltipWrapper msg="Open in Code Editor">
              <!-- svelte-ignore a11y-click-events-have-key-events -->
              <!-- svelte-ignore a11y-no-static-element-interactions -->
              <span
                class="text-blue-500 icon"
                on:click={() =>
                  executeRPC('openMacroInCodeEditor', [macro.path])}
              >
                <FaCode />
              </span>
            </TooltipWrapper>
          </Table.Cell>

          <Table.Cell>
            <TooltipWrapper msg="Schedule">
              <!-- svelte-ignore a11y-no-static-element-interactions -->
              <TaskSchedulerDialog macroPath={macro.path}>
                <!-- svelte-ignore a11y-click-events-have-key-events -->
                <span class="icon text-zinc-400">
                  <FaClock />
                </span>
              </TaskSchedulerDialog>
            </TooltipWrapper>
          </Table.Cell>
        </Table.Row>
      {/each}
    </Table.Body>
  </Table.Root>
</div>
