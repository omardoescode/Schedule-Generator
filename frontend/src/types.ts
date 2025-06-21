export enum SlotType {
	TUTORIAL = 'Tutorial',
	LECTURE = 'Lecture',
	LAB = 'Lab'
}

export enum DAY {
	SATURDAY = 'Saturday',
	SUNDAY = 'Sunday',
	MONDAY = 'Monday',
	TUESDAY = 'Tuesday',
	WEDNESDAY = 'Wednesday',
	THURSDAY = 'Thursday',
	FRIDAY = 'Friday'
}
export interface Time {
	hour: number;
	minute: number;
}
export interface Slot {
	day: DAY;
	start: Time;
	end: Time;
	type: SlotType;
}

export interface Course {
	title: string;
	required_slots: SlotType[];
	slots: Slot[];
	checked?: boolean;
}
