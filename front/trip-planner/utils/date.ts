export function getDateString(date: string | Date) {
  return new Date(date).toISOString().split('T')[0];
}

export function getDateTimeString(date: string | Date) {
  const offset = -new Date(date).getTimezoneOffset() * 60 * 1000;
  return new Date(new Date(date).getTime() + offset).toISOString().split('.')[0];
}

export function getLater(date: string | Date, days: number, hours: number = 0) {
  return new Date(new Date(date).getTime() + days * 24 * 60 * 60 * 1000 + hours * 60 * 60 * 1000);
}

export function getDaysFromTimestamp(timestamp: number) {
  return Math.floor(timestamp / (24 * 60 * 60 * 1000));
}

export function getHoursFromTimestamp(timestamp: number) {
  return Math.floor((timestamp % (24 * 60 * 60 * 1000)) / (60 * 60 * 1000));
}
