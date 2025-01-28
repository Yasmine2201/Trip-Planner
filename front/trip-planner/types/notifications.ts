export type Notifications = {
    notification_id: number,
    type: NotificationType,
    content: string,
    is_read: boolean,
    created_at: string,
}

export enum NotificationType {
    AddToTrip = 'AddToTrip',
    Budget = 'Budget',
    Invitation = 'Invitation',
}