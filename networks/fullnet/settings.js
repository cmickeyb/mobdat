{
    "General" :
    {
        "TimeSteps" : 0,
        "Interval" : 0.200,
        "SecondsPerStep" : 2.0,
        "StartTimeOfDay" : 3.0,
        "MaximumTravelers" : 0, 
	"WorldInfoFile" : "networks/fullnet/data/worldinfo.js",
        "Connectors" : ["opensim", "sumo", "social", "stats"]
    },

    "Builder" :
    {
	"ExtensionFiles" : ["networks/fullnet/layout.py", "networks/fullnet/business.py", "networks/fullnet/people.py"]
    },

    "SocialConnector" :
    {
        "WaitMean" : 1000.0,
        "WaitSigma" : 200.0,
        "PeopleCount" : 1200
    },

    "OpenSimConnector" :
    {
        "WorldSize" : [810.0, 810.0, 100.0],
        "WorldOffset" : [363.0, 363.0, 26.0],
        "WorldCenter" : [768.0, 768.0, 26.0],
        "Scale" : 0.6,
        "PositionDelta" : 0.1,
        "VelocityDelta" : 0.1,
        "AccelerationDelta" : 0.05,
        "EndPoint" : "http://127.0.0.1:7060/Dispatcher/",
        "Scene" : "Fullnet",
        "UpdateThreadCount" : 6,
        "Binary" : true
    },
    
    "SumoConnector" :
    {
	"SumoNetworkPath" : "networks/fullnet/net/",
	"SumoDataFilePrefix" : "network",
        "NetworkScaleFactor" : 10.0,
        "VehicleScaleFactor" : 4.0,
        "ConfigFile" : "networks/fullnet/fullnet.sumocfg",
        "ExtensionFiles" : [ ],
        "VelocityFudgeFactor" : 1.0,
        "SumoPort" : 8813
    },

    "StatsConnector" :
    {
        "CollectObjectDynamics" : true,
        "CollectObjectPattern" : "worker[357]+_trip.*"
    },

    "RoadTypes" :
    [
	{
	    "Name" : "Universal Road Segment",
	    "RoadTypes" : [ "etype1A", "etype1B", "etype1C",
                            "etype2A", "etype2B", "etype2C",
                            "etype3A", "etype3B", "etype3C",
                            "parking_entry", "driveway_road", "parking_drive",
                            "1way2lane", "1way3lane" ],
	    "ZOffset" : 20.5,
	    "AssetID" : { "ObjectName" : "SumoAssets Edges", "ItemName" : "Universal Road Segment" }
	}

    ],

    "IntersectionTypes" :
    [
	{
	    "Name" : "Universal Intersection [* * * *]",
	    "AssetID" : { "ObjectName" : "SumoAssets Nodes", "ItemName" : "Universal Intersection [* * * *]" },
	    "ZOffset" : 20.50,
	    "Padding" : 0.0,
	    "Signature" : ["*/*", "*/*", "*/*", "*/*"],
            "IntersectionTypes" : [ "driveway_node", "parking_drive_intersection", "apartment", "business", "townhouse", "stoplight", "priority" ]
	}
     ]
}
