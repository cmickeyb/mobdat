## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class BusinessProfile(Graph.Node) :

    # -----------------------------------------------------------------
    def __init__(self, name, biztype, joblist) :
        """
        Args:
            name -- string name of the profile
            biztype -- constant of type SocialDecoration.BusinessType
            joblist -- dictionary mapping type SocialDecoration.JobDescription --> Demand
        """
        Graph.Node.__init__(self, name = name)

        self.AddDecoration(SocialDecoration.BusinessProfileDecoration(biztype))
        self.AddDecoration(SocialDecoration.EmploymentProfileDecoration(joblist))

    # -----------------------------------------------------------------
    def AddServiceProfile(self, bizhours, capacity, servicetime) :
        """
        Args:
            bizhours -- object of type WeeklySchedule
            capacity -- integer maximum customer capacity
            servicetime -- float mean time to service a customer
        """
        self.AddDecoration(SocialDecoration.ServiceProfileDecoration(bizhours, capacity, servicetime))

## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class Business(Graph.Node) :

    # -----------------------------------------------------------------
    def __init__(self, name) :
        """
        Args:
            business -- object of type Business.Business
        """
        Graph.Node.__init__(self, name = name)

    # -----------------------------------------------------------------
    def SetResidence(self, location) :
        """
        Args:
            location -- object of type BusinessLocation
        """
        self.AddDecoration(SocialDecoration.ResidenceDecoration(location))

