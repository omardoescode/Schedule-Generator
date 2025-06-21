<script lang="ts">
	import { cubicOut } from "svelte/easing";
  import { slide, fade, scale } from "svelte/transition";
  export let title: string;
  export let open: boolean;
  export let onClose: () => void;
</script>

{#if open}
  <div transition:fade={{ duration: 300 }} class="fixed inset-0 z-50 bg-black opacity-90 flex items-center justify-center">
    <div
      class="flex items-center justify-center h-screen w-screen"
      on:click={(e) => {
        if (e.target === e.currentTarget) onClose();
      }}
    >
      <div
        transition:scale={{ duration: 300, easing: cubicOut }}
        class="relative rounded-lg bg-white shadow-2xl overflow-hidden w-full max-w-3xl"
      >
        <div class="flex justify-between items-center p-4 border-b">
          <h1 class="text-2xl font-semibold">{title}</h1>
          <button
            class="text-gray-700 hover:text-red-500 transition duration-200 pointer-cursor"
            on:click={onClose}
            transition:slide={{ duration: 200 }}
          >
            X
          </button>
        </div>
        <div class="p-4">
          <slot />
        </div>
      </div>
    </div>
  </div>
{/if}
