CREATE TABLE UserLogin (
                           userLoginId: uuid PRIMARY KEY,
                           email: string,
                           hashedPassword: string,
                           createdOn: timestamp,
                           emailConfirmedOn: timestamp
);

CREATE TABLE User (
                      userId: uuid,
                      alias: string,
                      firstname: string,
                      lastname: string,
                      birthdate: string,
                      profilePicture: uuid,
                      description: string
);

CREATE TABLE UserContact (
                             userContactId: uuid PRIMARY KEY,
                             userContactId :,
                             user1: string,
                             user2: string,
                             createdOn: timestamp,
                             status: enum
);

CREATE TABLE Visit (
                       visitId: uuid PRIMARY KEY,
                       locationId: uuid,
                       tripId: uuid,
                       visitName: string,
                       startDate: timestamp,
                       endDate: timestamp
);

CREATE TABLE Trip (
                      tripId: uuId PRIMARY KEY,
                      tripName: string,
                      startDate: date,
                      endDate: date,
                      center: geography,
                      radius: float,
                      imageId: uuid
);

CREATE TABLE Location (
                          locationId: uuid PRIMARY KEY,
                          locationName: string,
                          coordPlace: geography,
                          description: string
);

CREATE TABLE TripParticipation (
                                   tripParticiptationId: uuid PRIMARY KEY,
                                   userId: uuid,
                                   tripId: uuid,
                                   isOwner: boolean
);

CREATE TABLE LocationPrice (
                               priceId: uuid PRIMARY KEY,
                               locationId: uuid,
                               price: float,
                               priceName: string,
                               description: string,
                               createdOn: timestamp
);

CREATE TABLE Image (
                       imageId: uuid PRIMARY KEY,
                       name: string,
                       url: string,
                       size: int,
                       mimeType: string,
                       createdOn: timestamp
);

CREATE TABLE LocationPicture (
                                 locationId: uuid,
                                 imageId: uuid
);

CREATE TABLE Expense (
                         expenseId: uuid PRIMARY KEY,
                         budgetId: uuid,
                         categoryId: uuid,
                         name: string,
                         description: string,
                         plannedAmount: float,
                         realAmount: float,
                         isShared: boolean,
                         expenseGroup: uuid
);

CREATE TABLE ExpenseShare (
                              shareId: uuid PRIMARY KEY,
                              userId: uuid,
                              expenseId: uuid,
                              dueAmount: float,
                              refundAmount: float,
                              status: enum
);

CREATE TABLE ExpenseCategory (
                                 categoryId: uuid PRIMARY KEY,
                                 name: string
);

CREATE TABLE ExpenseGroup (
                              expenseGroupId: uuid PRIMARY KEY,
                              tripParticipationId: uuid,
    <div><span style="background-color:,
                              name: string,

);

CREATE TABLE Notification (
                              PRIMARY KEY,
                              userId: uuid,
                              title: string,
                              htmlContent: string,
                              createdOn: timestamp,
                              isRead: bool
);

CREATE TABLE TripInvitation (
                                PRIMARY KEY,
                                tripId: uuid,
                                userId: uuid,
                                status: enum
);

CREATE TABLE VisitParticipation (
                                    visitId: uuid,
                                    userId: uuid,
                                    status: enum
);