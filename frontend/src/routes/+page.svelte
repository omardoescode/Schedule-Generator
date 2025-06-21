<script lang="ts">
	import Accordion from '../components/accordion.svelte';
	import Dialog from '../components/dialog.svelte';
	import AddCourseForm from '../components/addcourseform.svelte';
	import CourseCard from '../components/coursecard.svelte';
	import { courses } from '../stores/courses';
	import { generateSchedule } from '../api';
	import { get } from 'svelte/store';
	import type { Course } from '../types';

	let addCourseDialogOpen: boolean = false;
	let editCourseDialogOpen: boolean = false;
	let courseToEditIndex: number | null = null;
	let courseToEdit: any = null;
	let schedules: any[] = [];
	let filteredSchedules: any[] = [];
	let maxCoursesInSchedule = 0;
	let loading = false;
	let error: string | null = null;
	let duplicateCourseIndex: number | null = null;
	let initialCourse: { title: string; required_slots: any[]; slots: any[] } | null = null;

	function openEditCourse(idx: number, course: any) {
		courseToEditIndex = idx;
		courseToEdit = course;
		editCourseDialogOpen = true;
	}

	// Add checked property to each course on add/duplicate
	function addCourseWithChecked(course: Course) {
		courses.update((cs) => [...cs, { ...course, checked: true }]);
	}

	function handleEditCourse(updatedCourse: Course) {
		courses.update((cs) =>
			cs.map((c, i) =>
				i === courseToEditIndex ? { ...updatedCourse, checked: c.checked ?? true } : c
			)
		);
		editCourseDialogOpen = false;
		courseToEditIndex = null;
		courseToEdit = null;
	}

	function removeCourse(idx: number) {
		courses.update((cs) => cs.filter((_, i) => i !== idx));
	}

	function handleDuplicateCourse(idx: number) {
		duplicateCourseIndex = idx;
		const course = get(courses)[idx];
		const newCourse = {
			title: '',
			required_slots: [...course.required_slots],
			slots: course.slots.map((s) => ({ ...s, start: { ...s.start }, end: { ...s.end } })),
			checked: true
		};
		initialCourse = newCourse;
		addCourseDialogOpen = true;
	}

	function toggleCourseChecked(idx: number) {
		courses.update((cs) => cs.map((c, i) => (i === idx ? { ...c, checked: !c.checked } : c)));
	}

	async function handleGenerate() {
		loading = true;
		error = null;
		schedules = [];
		try {
			const $courses = get(courses).filter((c) => c.checked ?? true);
			const result = await generateSchedule($courses);
			schedules = result;
		} catch (e) {
			error = e instanceof Error ? e.message : 'Unknown error';
		} finally {
			loading = false;
		}
	}

	$: if (schedules.length > 0) {
		maxCoursesInSchedule = Math.max(...schedules.map((s) => s.courses.length));
		const totalCourses = get(courses).length;
		const allCoursesSchedules = schedules.filter((s) => s.courses.length === totalCourses);
		filteredSchedules =
			allCoursesSchedules.length > 0
				? allCoursesSchedules
				: schedules.filter((s) => s.courses.length === maxCoursesInSchedule);
	} else {
		filteredSchedules = [];
		maxCoursesInSchedule = 0;
	}
</script>

<div class="min-h-screen bg-gradient-to-tr from-indigo-100 via-white to-pink-100 pb-20">
	<div class="mx-auto max-w-6xl px-4 py-12">
		<div class="mb-10 flex flex-col items-center justify-between gap-4 sm:flex-row">
			<h1 class="text-3xl font-extrabold tracking-tight text-indigo-800 drop-shadow-md sm:text-4xl">
				<span class="inline-block align-middle">📚</span> Your Courses
			</h1>
			<button
				on:click={() => (addCourseDialogOpen = true)}
				class="flex transform items-center gap-2 rounded-lg bg-indigo-600 px-6 py-3 text-lg font-bold text-white shadow-lg transition-transform hover:-translate-y-1 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-400 focus:ring-offset-2"
			>
				<svg class="h-6 w-6" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"
					><path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4" /></svg
				>
				Add Course
			</button>
		</div>

		<Dialog
			title={editCourseDialogOpen ? `Edit Course` : `Add a new course`}
			open={addCourseDialogOpen || editCourseDialogOpen}
			onClose={() => {
				addCourseDialogOpen = false;
				editCourseDialogOpen = false;
				initialCourse = null;
			}}
		>
			{#if editCourseDialogOpen}
				<AddCourseForm
					onAddCourse={handleEditCourse}
					initialCourse={courseToEdit}
					editMode={true}
					on:close={() => {
						addCourseDialogOpen = false;
						editCourseDialogOpen = false;
						initialCourse = null;
					}}
				/>
			{:else}
				<AddCourseForm
					onAddCourse={addCourseWithChecked}
					{initialCourse}
					editMode={false}
					on:close={() => {
						addCourseDialogOpen = false;
						editCourseDialogOpen = false;
						initialCourse = null;
					}}
				/>
			{/if}
		</Dialog>

		<!-- Courses Grid -->
		{#if $courses.length === 0}
			<div class="mt-20 text-center text-xl font-semibold text-gray-400">
				No courses yet. Add one!
			</div>
		{:else}
			<div class="mt-8 grid grid-cols-1 gap-8 sm:grid-cols-2 md:grid-cols-3">
				{#each $courses as course, i (course.title + '-' + i)}
					<CourseCard
						{course}
						onEdit={() => openEditCourse(i, course)}
						onRemove={() => removeCourse(i)}
						onDuplicate={() => handleDuplicateCourse(i)}
						checked={course.checked ?? true}
						onToggleChecked={() => toggleCourseChecked(i)}
					/>
				{/each}
			</div>
		{/if}

		{#if $courses.length > 0}
			<div class="mt-8 flex flex-col items-center">
				<button
					on:click={handleGenerate}
					class="mb-4 rounded-lg bg-pink-600 px-8 py-3 text-lg font-bold text-white shadow-lg hover:bg-pink-700 focus:outline-none focus:ring-2 focus:ring-pink-400 focus:ring-offset-2"
					disabled={loading}
				>
					{loading ? 'Generating...' : 'Generate Schedules'}
				</button>
				{#if error}
					<div class="font-semibold text-red-600">{error}</div>
				{/if}
				{#if schedules.length > 0}
					<div class="mt-6 w-full">
						<h2 class="mb-2 text-xl font-bold">
							Generated Schedules ({filteredSchedules.length})
							<span class="text-base font-normal text-gray-500"
								>(showing {maxCoursesInSchedule} course{maxCoursesInSchedule === 1 ? '' : 's'} per schedule)</span
							>
						</h2>
						<ul class="space-y-4">
							{#each filteredSchedules as sched, i}
								<li class="rounded bg-white p-4 shadow">
									<div class="mb-1 flex items-center gap-2 font-semibold">
										Schedule #{i + 1}
										<span
											class="ml-2 rounded bg-indigo-100 px-2 py-0.5 text-xs font-bold text-indigo-700"
											>{sched.courses.length} course{sched.courses.length === 1 ? '' : 's'}</span
										>
									</div>
									<ul class="ml-4 list-disc">
										{#each sched.courses as course}
											<li>
												<span class="font-bold">{course.name}</span>:
												<ul class="ml-4">
													{#each course.slots as slot}
														<li>
															{slot.slot_type} - {slot.day}, {slot.start.hour
																.toString()
																.padStart(2, '0')}:{slot.start.minute.toString().padStart(2, '0')} -
															{slot.end.hour.toString().padStart(2, '0')}:{slot.end.minute
																.toString()
																.padStart(2, '0')}
														</li>
													{/each}
												</ul>
											</li>
										{/each}
									</ul>
								</li>
							{/each}
						</ul>
					</div>
				{/if}
			</div>
		{/if}
	</div>
</div>
