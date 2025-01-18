export type Expense = {
    "expense_id": number,
    "name": string,
    "description": string,
    "planned_amount": number,
    "actual_amount": number,
    "is_shared": boolean,
    "category": string,
    "expense_group": object,
}