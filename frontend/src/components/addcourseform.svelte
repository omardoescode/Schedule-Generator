<script lang="ts">
	import { SlotType, DAY } from '../types';
	import { get } from 'svelte/store';
	import { courses } from '../stores/courses';
	import { toTimeString, fromTimeString } from '../lib/utils';
	import { createEventDispatcher } from 'svelte';

	export let onAddCourse: (course: {
		title: string;
		required_slots: SlotType[];
		slots: any[];
	}) => void;

	export let initialCourse: { title: string; required_slots: SlotType[]; slots: any[] } | null =
		null;
	export let editMode: boolean = false;

	const dispatch = createEventDispatcher();

	let title = '';
	let required_slots: SlotType[] = [];
	let slots = [
		{
			day: DAY.SUNDAY,
			start: { hour: 8, minute: 0 },
			end: { hour: 9, minute: 0 },
			type: SlotType.LECTURE
		}
	];
	let validationError: string | null = null;

	$: if (initialCourse) {
		title = initialCourse.title;
		required_slots = [...initialCourse.required_slots];
		slots = initialCourse.slots.map((s) => ({ ...s, start: { ...s.start }, end: { ...s.end } }));
	}

	function toggleSlotType(type: SlotType) {
		if (required_slots.includes(type)) {
			required_slots = required_slots.filter((t) => t !== type);
		} else {
			required_slots = [...required_slots, type];
		}
	}

	function addSlot() {
		slots = [
			...slots,
			{
				day: DAY.SUNDAY,
				start: { hour: 8, minute: 0 },
				end: { hour: 9, minute: 0 },
				type: SlotType.LECTURE
			}
		];
	}
	function removeSlot(idx: number) {
		if (slots.length > 1) {
			slots = slots.filter((_, i) => i !== idx);
		}
	}

	function handleSubmit(e: Event) {
		e.preventDefault();
		validationError = null;
		// Validation: every required_slot must have at least one slot of that type
		for (const type of required_slots) {
			if (!slots.some((s) => s.type === type)) {
				validationError = `You must add at least one slot for every required slot type (missing: ${type})`;
				return;
			}
		}
		// Validate unique course title
		const allCourses = get(courses);
		if (
			!editMode &&
			allCourses.some((c) => c.title.trim().toLowerCase() === title.trim().toLowerCase())
		) {
			validationError = 'A course with this name already exists.';
			return;
		}
		onAddCourse({ title, required_slots, slots });
		dispatch('close'); // Close dialog after submit
		if (!editMode) {
			// Optionally reset
			title = '';
			required_slots = [];
			slots = [
				{
					day: DAY.SUNDAY,
					start: { hour: 8, minute: 0 },
					end: { hour: 9, minute: 0 },
					type: SlotType.LECTURE
				}
			];
		}
	}
</script>

<form
	class="flex min-w-[320px] flex-col gap-6 rounded-xl bg-white p-8 shadow-md"
	on:submit={handleSubmit}
>
	{#if validationError}
		<div class="mb-2 font-semibold text-red-600">{validationError}</div>
	{/if}
	<div class="flex flex-col gap-1">
		<label for="title" class="mb-1 font-medium">Course Title</label>
		<input
			id="title"
			type="text"
			bind:value={title}
			required
			placeholder="e.g. Calculus I"
			class="w-full rounded-md border border-gray-300 px-3 py-2 text-base focus:outline-none focus:ring-2 focus:ring-indigo-400"
			{...editMode ? { disabled: true } : {}}
			on:keydown={(e) => {
				if (e.key === 'Enter') e.preventDefault();
			}}
		/>
	</div>

	<div class="flex flex-col gap-1" role="group" aria-labelledby="required-slot-types-label">
		<p id="required-slot-types-label" class="mb-1 font-medium">Required Slot Types</p>
		<div class="flex flex-wrap gap-4">
			{#each Object.values(SlotType) as type, idx}
				<label class="flex items-center gap-2 text-base">
					<input
						id={`slot-type-${idx}`}
						type="checkbox"
						checked={required_slots.includes(type)}
						on:change={() => toggleSlotType(type)}
						class="h-4 w-4 accent-indigo-500"
					/>
					{type}
				</label>
			{/each}
		</div>
	</div>

	<div class="flex flex-col gap-1" role="group" aria-labelledby="course-slots-label">
		<p id="course-slots-label" class="mb-1 font-medium">Course Slots</p>
		<div class="flex flex-col gap-2">
			{#each slots as slot, i}
				<div class="flex items-center gap-2 rounded-md bg-gray-50 px-3 py-2">
					<select
						id={`slot-day-${i}`}
						bind:value={slot.day}
						class="rounded-md border border-gray-300 px-2 py-1 focus:outline-none focus:ring-2 focus:ring-indigo-400"
					>
						{#each Object.values(DAY) as day}
							<option value={day}>{day}</option>
						{/each}
					</select>
					<select
						id={`slot-type-${i}`}
						bind:value={slot.type}
						class="rounded-md border border-gray-300 px-2 py-1 focus:outline-none focus:ring-2 focus:ring-indigo-400"
					>
						{#each Object.values(SlotType) as type}
							<option value={type}>{type}</option>
						{/each}
					</select>
					<input
						type="time"
						value={toTimeString(slot.start)}
						on:input={(e) =>
							(slot.start = fromTimeString((e.target as HTMLInputElement)?.value || '00:00'))}
						class="w-32 rounded-md border border-gray-300 px-2 py-1 text-base focus:outline-none focus:ring-2 focus:ring-indigo-400"
					/>
					<span class="mx-1">to</span>
					<input
						type="time"
						value={toTimeString(slot.end)}
						on:input={(e) =>
							(slot.end = fromTimeString((e.target as HTMLInputElement)?.value || '00:00'))}
						class="w-32 rounded-md border border-gray-300 px-2 py-1 text-base focus:outline-none focus:ring-2 focus:ring-indigo-400"
					/>
					<button
						type="button"
						class="ml-2 flex h-7 w-7 items-center justify-center rounded-full bg-red-100 text-red-600 transition hover:bg-red-200 disabled:cursor-not-allowed disabled:opacity-50"
						on:click={() => removeSlot(i)}
						disabled={slots.length === 1}>✖</button
					>
				</div>
			{/each}
		</div>
		<button
			type="button"
			class="mt-2 rounded-md bg-indigo-100 px-3 py-1 font-semibold text-indigo-700 transition hover:bg-indigo-200"
			on:click={addSlot}>+ Add Slot</button
		>
	</div>

	<button
		type="submit"
		class="mt-4 rounded-lg bg-indigo-700 px-6 py-2 text-lg font-bold text-white transition hover:bg-indigo-800"
		>{editMode ? 'Save Changes' : 'Add Course'}</button
	>
</form>
