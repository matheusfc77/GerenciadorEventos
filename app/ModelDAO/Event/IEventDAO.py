class IEventDAO:

    def getEventByName(self, event_name): raise NotImplementedError("EventDAO.getEventByName needs to be implemented")
    def getAllEvents(self, top): raise NotImplementedError("EventDAO.getAllEvents needs to be implemented")
    def insertEvents(self, events): raise NotImplementedError("EventDAO.insertEvent needs to be implemented")
    def updateAddress(self, event_name, new_values): raise NotImplementedError("EventDAO.updateAddress needs to be implemented")
    def deleteEvent(self, event_name): raise NotImplementedError("EventDAO.deleteEvent needs to be implemented")
