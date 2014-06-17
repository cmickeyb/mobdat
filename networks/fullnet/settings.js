{
    "General" :
    {
        "TimeSteps" : 0,
        "Interval" : 0.200,
        "SecondsPerStep" : 2.0,
        "StartTimeOfDay" : 0.0,
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
        "NetworkScaleFactor" : 16.0,
        "ConfigFile" : "networks/fullnet/fullnet.sumocfg",
        "ExtensionFiles" : [ ],
        "VelocityFudgeFactor" : 1.0,
        "SumoPort" : 8813
    },

    "RoadTypes" :
    [
	{
	    "Name" : "One Lane Road Segment",
	    "RoadTypes" : [ "etype1A", "etype1B", "etype1C" ],
	    "ZOffset" : 20.5,
	    "AssetID" : "7c3df98d-4b1e-4d35-92ec-f5bbad5f4596"
	},

	{
	    "Name" : "Two Lane Road Segment",
	    "RoadTypes" : [ "etype2A", "etype2B", "etype2C" ],
	    "ZOffset" : 20.5,
	    "AssetID" : "ee4f62a8-3311-4808-86f0-b6caa4d62ecc"
	},

	{
	    "Name" : "Road [20L]",
	    "RoadTypes" : [ "1way2lane" ],
	    "ZOffset" : 20.5,
	    "AssetID" : { "ObjectName" : "SumoAssets Edges", "ItemName" : "Road [20L]" }
	},

	{
	    "Name" : "Parking Lot Segment",
	    "RoadTypes" : ["parking_entry"],
	    "ZOffset" : 25.25,
	    "AssetID" : "b2b6c88f-e044-493e-a922-7da651138aae"
	},

	{
	    "Name" : "Marble Driveway",
	    "RoadTypes" : ["driveway"],
	    "ZOffset" : 20.5,
	    "AssetID" : "6d5ad1c2-54db-42a2-8544-b9117d3b1db5"
	},

	{
	    "Name" : "Asphalt Driveway",
	    "RoadTypes" : ["parking_drive"],
	    "ZOffset" : 25.25,
	    "AssetID" : "5147e8cf-41e5-480c-b9c3-0282bdb3867c"
	}

    ],

    "IntersectionTypes" :
    [
	{
	    "Name" : "Parking Lot Intersection [* P * P]",
	    "AssetID" : { "ObjectName" : "SumoAssets Nodes", "ItemName" : "Parking Lot Intersection [* P * P]" },
	    "ZOffset" : 20.50,
	    "Padding" : 2.5,
	    "Signature" : ["*/*", "*/*", "*/*", "*/*"],
            "IntersectionTypes" : [ "parking_drive_intersection" ]
	},

	{
	    "Name" : "ParkingLot Entry [00L 02L pp 20L]",
	    "AssetID" : { "ObjectName" : "SumoAssets Nodes", "ItemName" : "ParkingLot Entry [00L 02L PP 20L]" },
	    "ZOffset" : 20.5,
	    "Padding" : 5,
	    "Signature" : ["0L/2L", "P/P", "2L/0L", "0L/0L"],
            "IntersectionTypes" : [ "priority" ]
	},

	{
	    "Name" : "ParkingLot Entry [2L P 2L P]",
	    "AssetID" : { "ObjectName" : "SumoAssets Nodes", "ItemName" : "ParkingLot Entry [2L P 2L P]" },
	    "ZOffset" : 20.5,
	    "Padding" : 5,
	    "Signature" : ["P/P", "2L/2L", "P/P", "2L/2L"],
            "IntersectionTypes" : [ "priority" ]
	},

	{
	    "Name" : "ParkingLot Entry [2L P 2L P]",
	    "AssetID" : { "ObjectName" : "SumoAssets Nodes", "ItemName" : "ParkingLot Entry [2L P 2L P]" },
	    "ZOffset" : 20.5,
	    "Padding" : 5,
	    "Signature" : ["2L/2L", "0L/0L", "2L/2L", "P/P"],
            "IntersectionTypes" : [ "priority" ]
	},

	{
	    "Name" : "ParkingLot Entry [1L P 1L P]",
	    "AssetID" : { "ObjectName" : "SumoAssets Nodes", "ItemName" : "ParkingLot Entry [1L P 1L P]" },
	    "ZOffset" : 20.5,
	    "Padding" : 5,
	    "Signature" : ["1L/1L", "P/P", "1L/1L", "P/P"],
            "IntersectionTypes" : [ "priority" ]
	},

	{
	    "Name" : "ParkingLot Entry [1L P 1L 0L]",
	    "AssetID" : { "ObjectName" : "SumoAssets Nodes", "ItemName" : "ParkingLot Entry [1L P 1L 0L]" },
	    "ZOffset" : 20.5,
	    "Padding" : 5,
	    "Signature" : ["1L/1L", "P/P", "1L/1L", "0L/0L"],
            "IntersectionTypes" : [ "priority" ]
	},

	{
	    "Name" : "Intersection [00L 20L 20L 20L]",
	    "AssetID" : { "ObjectName" : "SumoAssets Nodes", "ItemName" : "Intersection [00L 20L 20L 20L]" },
	    "ZOffset" : 20.5,
	    "Padding" : 5,
	    "Signature" : ["0L/0L", "0L/2L", "1L/1L", "2L/0L"],
            "IntersectionTypes" : [ "stoplight", "priority" ]
	},

	{
	    "Name" : "Intersection [00L 20L 20L 00L] 1",
	    "AssetID" : { "ObjectName" : "SumoAssets Nodes", "ItemName" : "Intersection [00L 20L 20L 00L]" },
	    "ZOffset" : 20.5,
	    "Padding" : 5,
	    "Signature" : ["0L/0L", "2L/0L", "0L/2L", "0L/0L"],
            "IntersectionTypes" : [ "stoplight", "priority" ]
	},

	{
	    "Name" : "Intersection [00L 20L 20L 00L] 2",
	    "AssetID" : { "ObjectName" : "SumoAssets Nodes", "ItemName" : "Intersection [00L 20L 20L 00L]" },
	    "ZOffset" : 20.5,
	    "Padding" : 5,
	    "Signature" : ["0L/0L", "1L/1L", "0L/2L", "0L/0L"],
            "IntersectionTypes" : [ "stoplight", "priority" ]
	},

	{
	    "Name" : "Intersection [00L 20L 20L 00L] 3",
	    "AssetID" : { "ObjectName" : "SumoAssets Nodes", "ItemName" : "Intersection [00L 20L 20L 00L]" },
	    "ZOffset" : 20.5,
	    "Padding" : 5,
	    "Signature" : ["0L/0L", "1L/1L", "2L/0L", "0L/0L"],
            "IntersectionTypes" : [ "stoplight", "priority" ]
	},

	{
	    "Name" : "Intersection [00L 20L 20L 00L] 4",
	    "AssetID" : { "ObjectName" : "SumoAssets Nodes", "ItemName" : "Intersection [00L 20L 20L 00L]" },
	    "ZOffset" : 20.5,
	    "Padding" : 5,
	    "Signature" : ["0L/0L", "0L/2L", "1L/1L", "0L/0L"],
            "IntersectionTypes" : [ "stoplight", "priority" ]
	},

	{
	    "Name" : "Intersection [00L 20L 20L 00L] 5",
	    "AssetID" : { "ObjectName" : "SumoAssets Nodes", "ItemName" : "Intersection [00L 20L 20L 00L]" },
	    "ZOffset" : 20.5,
	    "Padding" : 5,
	    "Signature" : ["0L/0L", "0L/2L", "2L/0L", "0L/0L"],
            "IntersectionTypes" : [ "stoplight", "priority" ]
	},

	{
	    "Name" : "Intersection [20L 00L 02L 22L]",
	    "AssetID" : { "ObjectName" : "SumoAssets Nodes", "ItemName" : "Intersection [20L 00L 02L 22L]" },
	    "ZOffset" : 20.5,
	    "Padding" : 7.5,
	    "Signature" : ["2L/0L", "0L/0L", "0L/2L", "2L/2L"],
            "IntersectionTypes" : [ "stoplight", "priority" ]
	},

	{
	    "Name" : "Intersection [22L 20L 22L 02L]",
	    "AssetID" : { "ObjectName" : "SumoAssets Nodes", "ItemName" : "Intersection [22L 20L 22L 02L]" },
	    "ZOffset" : 20.5,
	    "Padding" : 7.5,
	    "Signature" : ["2L/2L", "0L/2L", "2L/2L", "2L/0L"],
            "IntersectionTypes" : [ "stoplight", "priority" ]
	},

	{
	    "Name" : "Intersection [0L, 0L, 1L, 2L]",
	    "AssetID" : { "ObjectName" : "SumoAssets Nodes", "ItemName" : "Intersection [0L, 0L, 1L, 2L]" },
	    "ZOffset" : 20.5,
	    "Padding" : 7.5,
	    "Signature" : ["0L/0L", "0L/0L", "1L/1L", "2L/2L"],
            "IntersectionTypes" : [ "stoplight", "priority" ]
	},

	{
	    "Name" : "Intersection [0L, 0L, 2L, 1L]",
	    "AssetID" : { "ObjectName" : "SumoAssets Nodes", "ItemName" : "Intersection [0L, 0L, 2L, 1L]" },
	    "ZOffset" : 20.5,
	    "Padding" : 7.5,
	    "Signature" : ["0L/0L", "0L/0L", "2L/2L", "1L/1L"],
            "IntersectionTypes" : [ "stoplight", "priority" ]
	},

	{
	    "Name" : "Intersection [0L 1L 1L 1L]",
	    "AssetID" : { "ObjectName" : "SumoAssets Nodes", "ItemName" : "Intersection [0L 1L 1L 1L]" },
	    "ZOffset" : 20.5,
	    "Padding" : 7.5,
	    "Signature" : ["0L/0L", "1L/1L", "1L/1L", "1L/1L"],
            "IntersectionTypes" : [ "stoplight", "priority" ]
	},

	{
	    "Name" : "Intersection [2L 0L 2L 1L]",
	    "AssetID" : { "ObjectName" : "SumoAssets Nodes", "ItemName" : "Intersection [2L 0L 2L 1L]" },
	    "ZOffset" : 20.5,
	    "Padding" : 7.5,
	    "Signature" : ["0L/0L", "2L/2L", "1L/1L", "2L/2L"],
            "IntersectionTypes" : [ "stoplight", "priority" ]
	},

	{
	    "Name" : "Intersection [2L 0L 2L 2L]",
	    "AssetID" : { "ObjectName" : "SumoAssets Nodes", "ItemName" : "Intersection [2L 0L 2L 2L]"},
	    "ZOffset" : 20.5,
	    "Padding" : 7.5,
	    "Signature" : ["0L/0L", "2L/2L", "2L/2L", "2L/2L"],
            "IntersectionTypes" : [ "stoplight", "priority" ]
	},

	{
	    "Name" : "Intersection [1L, 2L, 1L, 2L]",
	    "AssetID" : { "ObjectName" : "SumoAssets Nodes", "ItemName" : "Intersection [1L, 2L, 1L, 2L]" },
	    "ZOffset" : 20.5,
	    "Padding" : 7.5,
	    "Signature" : ["1L/1L", "2L/2L", "1L/1L", "2L/2L"],
            "IntersectionTypes" : [ "stoplight", "priority" ]
	},

	{
	    "Name" : "Intersection [1L, 2L, 2L, 2L]",
	    "AssetID" : { "ObjectName" : "SumoAssets Nodes", "ItemName" : "Intersection [1L, 2L, 2L, 2L]" },
	    "ZOffset" : 20.5,
	    "Padding" : 7.5,
	    "Signature" : ["1L/1L", "2L/2L", "2L/2L", "2L/2L"],
            "IntersectionTypes" : [ "stoplight", "priority" ]
	},

	{
	    "Name" : "Intersection [2L 2L 2L 2L]",
	    "AssetID" : { "ObjectName" : "SumoAssets Nodes", "ItemName" : "Intersection [2L 2L 2L 2L]" },
	    "ZOffset" : 20.5,
	    "Padding" : 7.5,
	    "Signature" : ["2L/2L", "2L/2L", "2L/2L", "2L/2L"],
            "IntersectionTypes" : [ "stoplight", "priority" ]
	},

	{
	    "Name" : "Intersection [1L 1L 1L 1L]",
	    "AssetID" : { "ObjectName" : "SumoAssets Nodes", "ItemName" : "Intersection [1L 1L 1L 1L]" },
	    "ZOffset" : 20.5,
	    "Padding" : 7.5,
	    "Signature" : ["1L/1L", "1L/1L", "1L/1L", "1L/1L"],
            "IntersectionTypes" : [ "stoplight", "priority" ]
	},

	{
	    "Name" : "Intersection [1L 2L 1L 2L]",
	    "AssetID" : { "ObjectName" : "SumoAssets Nodes", "ItemName" : "Intersection [1L 1L 1L 1L]" },
	    "ZOffset" : 20.5,
	    "Padding" : 7.5,
	    "Signature" : ["1L/1L", "2L/0L", "1L/1L", "0L/2L"],
            "IntersectionTypes" : [ "stoplight", "priority" ]
	},
	    
	{
	    "Name" : "Intersection [1L 0L 1L 2L]",
	    "AssetID" : { "ObjectName" : "SumoAssets Nodes", "ItemName" : "Intersection [1L 0L 1L 2L]" },
	    "ZOffset" : 20.5,
	    "Padding" : 7.5,
	    "Signature" : ["1L/1L", "0L/0L", "1L/1L", "2L/2L"],
            "IntersectionTypes" : [ "stoplight", "priority" ]
	},
	
	{
	    "Name" : "Intersection [1L 1L 1L 2L]",
	    "AssetID" : { "ObjectName" : "SumoAssets Nodes", "ItemName" : "Intersection [1L 1L 1L 2L]" },
	    "ZOffset" : 20.5,
	    "Padding" : 7.5,
	    "Signature" : ["1L/1L", "1L/1L", "1L/1L", "2L/2L"],
            "IntersectionTypes" : [ "stoplight", "priority" ]
	},

	{
	    "Name" : "Intersection [0L 0L 1L 1L]",
	    "AssetID" : { "ObjectName" : "SumoAssets Nodes", "ItemName" : "Intersection [0L 0L 1L 1L]" },
	    "ZOffset" : 20.5,
	    "Padding" : 7.5,
	    "Signature" : ["0L/0L", "0L/0L", "1L/1L", "1L/1L"],
            "IntersectionTypes" : [ "stoplight", "priority" ]
	},

	{
	    "Name" : "Intersection [0L 0L 2L 2L]",
	    "AssetID" : { "ObjectName" : "SumoAssets Nodes", "ItemName" : "Intersection [0L 0L 2L 2L]" },
	    "ZOffset" : 20.5,
	    "Padding" : 7.5,
	    "Signature" : ["0L/0L", "0L/0L", "2L/2L", "2L/2L"],
            "IntersectionTypes" : [ "stoplight", "priority" ]
	},

	{
	    "Name" : "Residential Row 1way 1lane",
	    "AssetID" : { "ObjectName" : "SumoAssets Nodes", "ItemName" : "Residential Row 1way 1lane" },
	    "ZOffset" : 25.0,
	    "Padding" : 0,
	    "Signature" : ["0L/0L", "0L/0L", "D/D", "0L/0L"],
            "IntersectionTypes" : [ "townhouse", "apartment" ]
	},

	{
	    "Name" : "Residential 1way 1lane",
	    "AssetID" : { "ObjectName" : "SumoAssets Nodes", "ItemName" : "Residential 1way 1lane" },
	    "ZOffset" : 25.4,
	    "Padding" : 0,
	    "Signature" : ["0L/0L", "0L/0L", "D/D", "0L/0L"],
            "IntersectionTypes" : [ ],
            "xIntersectionTypes" : [ "townhouse" ]
	},

        {
            "Name" : "Business Box [D 0L 0L 0L]",
	    "AssetID" : { "ObjectName" : "SumoAssets Nodes", "ItemName" : "Business Box [D 0L 0L 0L]" },
            "ZOffset" : 26.0,
            "Padding" : 0,
            "Signature" : ["D/D", "0L/0L", "0L/0L", "0L/0L"],
            "IntersectionTypes" : ["business"]
        },

	{
	    "Name" : "Intersection 2Lane Driveway",
	    "AssetID" : { "ObjectName" : "SumoAssets Nodes", "ItemName" : "Intersection 2Lane Driveway" },
	    "ZOffset" : 20.5,
	    "Padding" : 2.5,
	    "Signature" : ["1L/1L", "D/D", "1L/1L", "D/D"],
            "IntersectionTypes" : [ "driveway" ]
	},

	{
	    "Name" : "Intersection 2Lane Driveway",
	    "AssetID" : { "ObjectName" : "SumoAssets Nodes", "ItemName" : "Intersection 2Lane Driveway" },
	    "ZOffset" : 20.5,
	    "Padding" : 2.5,
	    "Signature" : ["1L/1L", "0L/0L", "1L/1L", "D/D"],
            "IntersectionTypes" : [ "driveway" ]
	},

	{
	    "Name" : "Intersection 2Lane Driveway",
	    "AssetID" : { "ObjectName" : "SumoAssets Nodes", "ItemName" : "Intersection 2Lane Driveway" },
	    "ZOffset" : 20.5,
	    "Padding" : 2.5,
	    "Signature" : ["1L/1L", "0L/0L", "1L/1L", "0L/0L"],
            "IntersectionTypes" : [ "driveway" ]
	},

	{
	    "Name" : "Intersection 2Lane Driveway",
	    "AssetID" : { "ObjectName" : "SumoAssets Nodes", "ItemName" : "Intersection 2Lane Driveway" },
	    "ZOffset" : 20.5,
	    "Padding" : 2.5,
	    "Signature" : ["1L/1L", "0L/0L", "0L/0L", "1L/1L"],
            "IntersectionTypes" : [ "driveway" ]
	},

	{
	    "Name" : "Intersection 2Lane Driveway",
	    "AssetID" : { "ObjectName" : "SumoAssets Nodes", "ItemName" : "Intersection 2Lane Driveway" },
	    "ZOffset" : 20.5,
	    "Padding" : 2.5,
	    "Signature" : ["1L/1L", "1L/1L", "0L", "1L/1L"],
            "IntersectionTypes" : [ "driveway" ]
	},

	{
	    "Name" : "Intersection 4Lane Driveway",
	    "AssetID" : { "ObjectName" : "SumoAssets Nodes", "ItemName" : "Intersection 4Lane Driveway" },
	    "ZOffset" : 20.5,
	    "Padding" : 5,
	    "Signature" : ["2L/2L", "D/D", "2L/2L", "D/D"],
            "IntersectionTypes" : [ "driveway" ]
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
            "StartParameter" : "{ 'terminate' : 0, 'color' : '<0.0, 0.0, 1.0>', 'scale' : '<0.75, 3.0, 0.75>' }"
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
            "StartParameter" : "{ 'terminate' : 0, 'color' : '<1.0, 0.5, 0.0>', 'scale' : '<0.75, 2.0, 0.75>' }"
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
            "StartParameter" : "{ 'terminate' : 0, 'color' : '<1.0, 0.0, 1.0>', 'scale' : '<0.75, 2.0, 0.75>' }"
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
            "StartParameter" : "{ 'terminate' : 0, 'color' : '<1.0, 0.0, 0.0>', 'scale' : '<0.75, 3.0, 0.75>' }"
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
            "StartParameter" : "{ 'terminate' : 0, 'color' : '<0.0, 1.0, 0.0>', 'scale' : '<1.25, 4.0, 1.25>' }"
        }
    ]
}
