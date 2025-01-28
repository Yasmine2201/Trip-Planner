export default function getNotificationProps(notificationContent, t) {
  return {
    'AddToTrip': {
      label: t('notifications.type.add-to-trip'),
      icon: 'material-symbols:trip-outline',
      link: () => `/home/trips/${notificationContent.data.tripId}`
    },
    'Budget': {
      label: t('notifications.type.budget'),
      icon: 'material-symbols:currency-exchange',
      link: () => `/home/trips/${notificationContent.data.tripId}/budget`
    },
    'Invitation': {
        label: t('notifications.type.invitation'),
        icon: 'ic:outline-markunread-mailbox',
        link: () => `/home/invitations`
    }
  }
}