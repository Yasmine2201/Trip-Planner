import type {Visit} from "~/types/visits";

export type Expense = {
    "expense_id": number,
    "name": string,
    "description": string,
    "planned_amount": number,
    "actual_amount": number,
    "category": string,
    "visit": Pick<Visit, 'visit_id' | 'name'>
}