<script lang="ts">
	export let course: any;
	export let onEdit: (course: any) => void;
	export let onRemove: () => void;
	export let onDuplicate: () => void;
	export let checked: boolean;
	export let onToggleChecked: () => void;
</script>

<div
	class="flex max-w-[480px] flex-col gap-4 rounded-2xl border border-indigo-200 bg-white p-6 shadow-xl transition-all hover:shadow-2xl"
>
	<div class="mb-2 flex items-center gap-2">
		<input
			type="checkbox"
			{checked}
			on:change={onToggleChecked}
			class="mr-2 h-5 w-5 accent-indigo-600"
		/>
		<div
			class="flex h-10 w-10 items-center justify-center rounded-full bg-indigo-100 text-2xl font-bold text-indigo-600"
		>
			{course.title.charAt(0)}
		</div>
		<div>
			<div class="text-lg font-extrabold text-indigo-800">{course.title}</div>
			<div class="text-xs text-gray-400">
				{course.required_slots.length} required slot{course.required_slots.length === 1 ? '' : 's'}
			</div>
		</div>
	</div>
	<div>
		<div class="mb-1 font-semibold text-gray-700">Required Slot Types:</div>
		<div class="flex flex-wrap gap-2">
			{#if course.required_slots.length > 0}
				{#each course.required_slots as type}
					<span
						class="rounded border border-indigo-200 bg-indigo-50 px-2 py-1 text-xs font-bold text-indigo-700"
						>{type}</span
					>
				{/each}
			{:else}
				<span class="text-xs text-gray-400">None</span>
			{/if}
		</div>
	</div>
	<div>
		<div class="mb-1 font-semibold text-gray-700">Slots:</div>
		<ul class="space-y-1">
			{#each course.slots as slot}
				<li class="flex items-center gap-2 text-sm text-gray-800">
					<span class="inline-block font-bold text-indigo-600">{slot.type}</span>
					<span class="rounded bg-gray-100 px-2 py-0.5 text-xs text-gray-600">{slot.day}</span>
					<span class="text-xs">
						{slot.start.hour.toString().padStart(2, '0')}:{slot.start.minute
							.toString()
							.padStart(2, '0')} - {slot.end.hour.toString().padStart(2, '0')}:{slot.end.minute
							.toString()
							.padStart(2, '0')}
					</span>
				</li>
			{/each}
		</ul>
	</div>
	<div class="mt-2 flex gap-2 self-end">
		<button
			class="rounded bg-indigo-100 px-3 py-1 text-xs font-bold text-indigo-700 transition hover:bg-indigo-200"
			on:click={() => onEdit(course)}>Edit</button
		>
		<button
			class="rounded bg-green-100 px-3 py-1 text-xs font-bold text-green-700 transition hover:bg-green-200"
			on:click={onDuplicate}>Duplicate</button
		>
		<button
			class="rounded bg-red-100 px-3 py-1 text-xs font-bold text-red-700 transition hover:bg-red-200"
			on:click={onRemove}>Remove</button
		>
	</div>
</div>
