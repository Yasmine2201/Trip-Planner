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
    'InvitationReceived': {
        label: t('notifications.type.invitation-received'),
        icon: 'ic:outline-markunread-mailbox',
        link: () => `/home/invitations`
    },
    'InvitationAccepted': {
        label: t('notifications.type.invitation-accepted'),
        icon: 'material-symbols:check-circle-outline',
        link: () => `/home/trips/${notificationContent.data.tripId}/members`
    },
    'InvitationDeclined': {
        label: t('notifications.type.invitation-declined'),
        icon: 'material-symbols:cancel-outline',
        link: () => `/home/trips/${notificationContent.data.tripId}/members`
    }
  }
}