import {z} from 'zod';

export enum CategoryValues {
    ACCOMMODATION = 'Accommodation',
    FOOD = 'Food',
    TRANSPORT = 'Transport',
    ACTIVITY = 'Activity',
    SHOPPING = 'Shopping',
    VISIT = 'Visit',
    OTHERS = 'Others',
}

export const expenseSchema = z.object({
    category: z.nativeEnum(CategoryValues, {message: 'errors.category-required'}),
    name: z.string({required_error: 'errors.name-required'}).max(255, {message: 'errors.name-too-long'}),
    description: z.string().max(100, {message: 'errors.description-too-long'}).optional(),
    planned_amount: z.number({invalid_type_error: 'errors.must-be-number'}).nonnegative({message: 'errors.planned-amount-positive'}).optional(),
    actual_amount: z.number({invalid_type_error: 'errors.must-be-number'}).nonnegative({message: 'errors.planned-amount-positive'}).optional(),
    visit_id: z.number({message: 'errors.must-be-number'}).optional(),
});

export type ExpenseDto = z.input<typeof expenseSchema>;

export const budgetSchema = z.object({
    budget: z.number({invalid_type_error: 'errors.must-be-number'}).nonnegative({message: 'errors.budget-positive'}),
});

export type BudgetDto = z.input<typeof budgetSchema>;