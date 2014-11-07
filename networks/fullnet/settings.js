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
     ],

    "VehicleTypes" :
    [
        {
            "Name" : "BlueCar",
            "Description" : "A blue car",
            "Rate" : 15,
            "ProfileTypes" : ["worker", "student", "homemaker"],
	    "Acceleration" : 0.3,
	    "Deceleration" : 0.3,
	    "Sigma" : 0.5,
	    "Length" : 3,
	    "MinGap" : 2,
	    "MaxSpeed" : 2.0,
            "AssetID" : "65715f46-7dc1-4b4a-ba64-23b9f972bdc4",
            "StartParameter" : "{ 'terminate' : 0, 'color' : '<0.0, 0.0, 1.0>', 'scale' : '<0.65, 1.5, 0.65>' }"
        },

        {
            "Name" : "OrangeCar",
            "Description" : "An orange car",
            "Rate" : 15,
            "ProfileTypes" : ["worker", "student", "homemaker"],
	    "Acceleration" : 0.8,
	    "Deceleration" : 0.8,
	    "Sigma" : 0.5,
	    "Length" : 2,
	    "MinGap" : 2,
	    "MaxSpeed" : 4.0,
            "AssetID" : "65715f46-7dc1-4b4a-ba64-23b9f972bdc4",
            "StartParameter" : "{ 'terminate' : 0, 'color' : '<1.0, 0.5, 0.0>', 'scale' : '<0.65, 1.0, 0.65>' }"
        },
        
        {
            "Name" : "PurpleCar",
            "Description" : "A purple car",
            "Rate" : 15,
            "ProfileTypes" : ["worker", "student", "homemaker"],
	    "Acceleration" : 0.2,
	    "Deceleration" : 0.2,
	    "Sigma" : 0.5,
	    "Length" : 2,
	    "MinGap" : 2,
	    "MaxSpeed" : 1.2,
            "AssetID" : "65715f46-7dc1-4b4a-ba64-23b9f972bdc4",
            "StartParameter" : "{ 'terminate' : 0, 'color' : '<1.0, 0.0, 1.0>', 'scale' : '<0.65, 1.0, 0.65>' }"
        },
        
        {
            "Name" : "RedCar",
            "Description" : "A red car",
            "Rate" : 15,
            "ProfileTypes" : ["worker", "student", "homemaker"],
	    "Acceleration" : 0.4,
	    "Deceleration" : 0.4,
	    "Sigma" : 0.5,
	    "Length" : 3,
	    "MinGap" : 2,
	    "MaxSpeed" : 3.0,
            "AssetID" : "65715f46-7dc1-4b4a-ba64-23b9f972bdc4",
            "StartParameter" : "{ 'terminate' : 0, 'color' : '<1.0, 0.0, 0.0>', 'scale' : '<0.65, 1.75, 0.65>' }"
        },

        {
            "Name" : "Van",
            "Description" : "A green van",
            "Rate" : 5,
            "ProfileTypes" : ["worker", "student", "homemaker"],
	    "Acceleration" : 0.2,
	    "Deceleration" : 0.2,
	    "Sigma" : 0.5,
	    "Length" : 4,
	    "MinGap" : 2,
	    "MaxSpeed" : 1.0,
            "AssetID" : "65715f46-7dc1-4b4a-ba64-23b9f972bdc4",
            "StartParameter" : "{ 'terminate' : 0, 'color' : '<0.0, 1.0, 0.0>', 'scale' : '<1.0, 2.0, 1.0>' }"
        }
    ]
}
