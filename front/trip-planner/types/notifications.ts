export type Notifications = {
    notification_id : number,
    type : string,
    content : string,
    is_read : boolean,
    created_at : string,
}
export enum NotificationType {// pay attention : the keys are case sensitive
  Info = 'i-heroicons-information-circle',
  Budget = 'material-symbols:currency-exchange',
  Invitation = 'material-symbols:contact-mail-sharp'
}