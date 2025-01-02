import { z } from 'zod';

export const createTripSchema = z.object({
    tripName: z.string().min(1, { message: 'errors.trip-name-required' }),
    latitude: z.number().min(-90).max(90, { message: 'errors.invalid-coordinates' }),
    longitude: z.number().min(-180).max(180, { message: 'errors.invalid-coordinates' }),
    radius: z.number().positive({ message: 'errors.radius-required' }),
    start_date: z.string().refine((value) => {
        const start = new Date(value);
        return !isNaN(start.getTime());
    }, { message: 'errors.invalid-start-date' }),
    end_date: z.string().refine((value) => {
        const end = new Date(value);
        return !isNaN(end.getTime());
    }, { message: 'errors.invalid-end-date' }),
}).refine((data) => {
    const start_date = new Date(data.start_date);
    const end_date = new Date(data.end_date);
    return start_date <= end_date;
}, {
    message: 'errors.start-date-before-end-date',
    path: ['end_date'],
});

export type CreateTripDto = z.input<typeof createTripSchema>;
