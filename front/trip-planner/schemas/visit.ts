import { z } from 'zod';

export const createVisitSchema = z.object({
    name: z.string().min(1, { message: 'errors.visit-name-required' }),
    start_date: z.string().refine((value) => {
        const start = new Date(value);
        return !isNaN(start.getTime());
    }, { message: 'errors.invalid-start-date' }),
    end_date: z.string().refine((value) => {
        const end = new Date(value);
        return !isNaN(end.getTime());
    }, { message: 'errors.invalid-end-date' }),
    place: z.object({
        latitude: z.number().min(-90).max(90, { message: 'errors.invalid-coordinates' }),
        longitude: z.number().min(-180).max(180, { message: 'errors.invalid-coordinates' }),
        radius: z.number().positive({ message: 'errors.radius-required' }),
    }).nullable(),
    trip_id: z.string().uuid({ message: 'errors.invalid-trip-id' }),
}).refine((data) => {
    const start_date = new Date(data.start_date);
    const end_date = new Date(data.end_date);
    return start_date <= end_date;
}, {
    message: 'errors.start-date-before-end-date',
    path: ['end_date'],
});

export type CreateVisitDto = z.input<typeof createVisitSchema>;

const modifyVisitSchema: z.ZodType<CreateVisitDto> = createVisitSchema.sourceType().extend({
    visit_id: z.string().uuid({ message: 'errors.invalid-visit-id' }),
});

export type ModifyVisitDto = z.input<typeof modifyVisitSchema>;
