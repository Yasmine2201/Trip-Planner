import { z } from 'zod';

export enum CategoryValues {
  ACCOMMODATION = 'Accommodation',
  FOOD = 'Food',
  TRANSPORT = 'Transport',
  ACTIVITY = 'Activity',
  OTHERS = 'Others',
}

export const expenseSchema = z.object({
  category : z.nativeEnum(CategoryValues, { message: 'errors.category-required' }),
  name: z.string({required_error: 'errors.name-required'}).max(20, { message: 'errors.name-too-long' }),
  description: z.string().max(100, { message: 'errors.description-too-long' }).optional(),
  planned_amount: z.number({invalid_type_error: 'errors.must-be-number'}).positive({ message: 'errors.planned-amount-positive' }).optional(),
  actual_amount: z.number({invalid_type_error: 'errors.must-be-number'}).positive({ message: 'errors.planned-amount-positive' }).optional(),
  is_shared: z.boolean(),
  expense_group: z.number({message: 'errors.must-be-number'}).optional(),
});

export type ExpenseDto = z.input<typeof expenseSchema>;
