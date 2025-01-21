import { z } from 'zod';

export enum CategoryValues {
  ACCOMMODATION = 'Accommodation',
  FOOD = 'Food',
  TRANSPORT = 'Transport',
  ACTIVITY = 'Activity',
  OTHERS = 'Others',
}

export const expenseSchema = z.object({
  category : z.nativeEnum(CategoryValues),
  name: z.string().min(1, { message: 'errors.name-required' }).max(20, { message: 'errors.name-too-long' }),
  description: z.string().max(100, { message: 'errors.description-too-long' }).optional(),
  planned_amount: z.number({message: 'errors.must-be-number'}).positive({ message: 'errors.planned-amount-positive' }).optional(),
  actual_amount: z.number({message: 'errors.must-be-number'}).positive({ message: 'errors.actual-amount-positive' }),
  is_shared: z.boolean(),
  expense_group: z.number({message: 'errors.must-be-number'}).optional(),
});

export type ExpenseDto = z.input<typeof expenseSchema>;
