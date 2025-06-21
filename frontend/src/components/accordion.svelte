<script lang="ts">
	import { slide } from 'svelte/transition';
	export let label: string;

	let open = false;
	const handleOpen = () => (open = !open);
</script>

<div class="rounded-xl shadow-md bg-white border border-gray-200 transition-all">
  <button
    type="button"
    class="w-full flex items-center justify-between px-5 py-4 bg-indigo-600 text-white font-semibold text-lg focus:outline-none hover:bg-indigo-700 transition"
    on:click={handleOpen}
    aria-expanded={open}
    aria-controls="accordion-content"
  >
    <span>{label}</span>
    <svg
      class="w-6 h-6 transform transition-transform duration-200"
      style="transform: rotate({open ? 180 : 0}deg);"
      fill="none"
      stroke="currentColor"
      viewBox="0 0 24 24"
      xmlns="http://www.w3.org/2000/svg"
    >
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
    </svg>
  </button>
  {#if open}
    <div
      id="accordion-content"
      class="bg-gray-50 px-5 py-4 border-t border-gray-200 animate-fadeIn"
      transition:slide={{ duration: 200 }}
    >
      <slot />
    </div>
  {/if}
</div>

<style>
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
.animate-fadeIn {
  animation: fadeIn 0.2s ease;
}
</style>
