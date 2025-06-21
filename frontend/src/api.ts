// Backend API base URL (adjust if needed)
const API_BASE = 'http://localhost:8000';

import type { Course } from './types';

export async function ping(): Promise<{ ping: string }> {
	const res = await fetch(`${API_BASE}/ping`);
	if (!res.ok) throw new Error('Ping failed');
	return res.json();
}

export async function generateSchedule(courses: Course[]): Promise<any[]> {
	// Backend expects: name, slots, slot_types
	const payload = courses.map((c) => ({
		name: c.title,
		slots: c.slots.map((s) => ({
			day: s.day.toUpperCase(),
			start: s.start,
			end: s.end,
			slot_type: s.type.toUpperCase()
		})),
		slot_types: c.required_slots.map((t) => t.toUpperCase())
	}));
	const res = await fetch(`${API_BASE}/schedule`, {
		method: 'POST',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify(payload)
	});
	console.log(res.status);
	if (!res.ok) throw new Error('Schedule generation failed');
	return res.json();
}
