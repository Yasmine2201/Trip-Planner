export type Notifications = {
    notification_id : number,
    type : string,
    content : string,
    is_read : boolean,
    created_at : string,
}
export enum NotificationType {
  info = 'i-heroicons-information-circle',
  budget = 'material-symbols:currency-exchange',
  invitation = 'material-symbols:contact-mail-sharp'
}