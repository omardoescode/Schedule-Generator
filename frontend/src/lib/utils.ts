// Utility functions for time formatting
export function toTimeString(time: { hour: number; minute: number }): string {
	return `${time.hour.toString().padStart(2, '0')}:${time.minute.toString().padStart(2, '0')}`;
}

export function fromTimeString(str: string): { hour: number; minute: number } {
	const [hour, minute] = str.split(':').map(Number);
	return { hour, minute };
}
