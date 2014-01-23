{
    "General" :
    {
        "TimeSteps" : 2000,
        "Interval" : 0.100,
        "Connectors" : ["opensim", "sumo", "social", "stats"]
    },

    "NetworkBuilder" :
    {
	"InjectionPrefix" : "IN",
	"ExtensionFiles" : ["networks/fullnet/builder.py"]
    },

    "SocialConnector" :
    {
	"NodeDataFile" : "networks/fullnet/nodedata.js",
        "WaitMean" : 1000.0,
        "WaitSigma" : 200.0,
        "PeopleCount" : 1200
    },

    "OpenSimConnector" :
    {
        "WorldSize" : [810.0, 810.0, 100.0],
        "WorldOffset" : [107.0, 107.0, 26.0],
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
        "NetworkScaleFactor" : 8.0,
        "ConfigFile" : "networks/fullnet/fullnet.sumocfg",
        "ExtensionFiles" : [ ],
        "VelocityFudgeFactor" : 1.0,
        "SumoPort" : 8813
    },

    "RoadTypes" :
    [
	{
	    "Name" : "One Lane Road Segment",
	    "EdgeTypes" : [ "etype1A", "etype1B", "etype1C" ],
	    "ZOffset" : 20.5,
	    "AssetID" : "3b155bd7-074b-4347-bfd2-c1e232a33e55"
	},

	{
	    "Name" : "Two Lane Road Segment",
	    "EdgeTypes" : [ "etype2A", "etype2B", "etype2C" ],
	    "ZOffset" : 20.5,
	    "AssetID" : "8e621d4b-d067-4d69-ba48-748997b73aa6"
	},

	{
	    "Name" : "Parking Lot Segment",
	    "EdgeTypes" : ["parking_entry"],
	    "ZOffset" : 25.25,
	    "AssetID" : "ea5280c4-d2e5-4d40-b4cc-6f05a36a6dae"
	},

	{
	    "Name" : "Marble Driveway",
	    "EdgeTypes" : ["driveway"],
	    "ZOffset" : 20.5,
	    "AssetID" : "f51c1812-0d8c-4e1e-b2ac-fea6756d908a"
	},

	{
	    "Name" : "Asphalt Driveway",
	    "EdgeTypes" : ["parking_drive"],
	    "ZOffset" : 25.25,
	    "AssetID" : "85265a47-e1a9-4f28-8425-88f29d8409b6"
	}

    ],

    "NodeTypes" :
    [
	{
	    "Name" : "Parking Lot Intersection [* P * P]",
	    "AssetID" : "685018da-1f1d-47df-a85a-61086c12e715",
	    "ZOffset" : 25.25,
	    "Padding" : 2.5,
	    "Signature" : ["*", "*", "*", "*"],
            "NodeTypes" : [ "parking_drive_intersection" ]
	},

	{
	    "Name" : "ParkingLot Entry [2L P 2L P]",
	    "AssetID" : "46dc7390-8401-4b74-a76b-82eb43dd8531",
	    "ZOffset" : 20.5,
	    "Padding" : 5,
	    "Signature" : ["1L", "P", "1L", "P"],
            "NodeTypes" : [ "priority" ]
	},

	{
	    "Name" : "ParkingLot Entry [2L P 2L 0L]",
	    "AssetID" : "8dc50ef2-cea4-4dea-9647-02ade0ade752",
	    "ZOffset" : 20.5,
	    "Padding" : 5,
	    "Signature" : ["1L", "P", "1L", "0L"],
            "NodeTypes" : [ "priority" ]
	},

	{
	    "Name" : "Intersection [0L, 0L, 1L, 2L]",
	    "AssetID" : "a7588c14-b555-4d09-9190-8cb0d4221388",
	    "ZOffset" : 20.5,
	    "Padding" : 15,
	    "Signature" : ["0L", "0L", "1L", "2L"],
            "NodeTypes" : [ "stoplight", "priority" ]
	},

	{
	    "Name" : "Intersection [0L, 0L, 2L, 1L]",
	    "AssetID" : "44a318a4-2df2-4461-ac60-81eeaa6a4ec5",
	    "ZOffset" : 20.5,
	    "Padding" : 15,
	    "Signature" : ["0L", "0L", "2L", "1L"],
            "NodeTypes" : [ "stoplight", "priority" ]
	},

	{
	    "Name" : "Intersection [0L 1L 1L 1L]",
	    "AssetID" : "e598dd5e-f0d9-4d73-818b-617aef753675",
	    "ZOffset" : 20.5,
	    "Padding" : 7.5,
	    "Signature" : ["0L", "1L", "1L", "1L"],
            "NodeTypes" : [ "stoplight", "priority" ]
	},

	{
	    "Name" : "Intersection 3way 4lane by 2lane",
	    "AssetID" : "69e601e3-f8b4-4ab0-8c49-5e8c0bee5ad8",
	    "ZOffset" : 20.5,
	    "Padding" : 15,
	    "Signature" : ["0L", "2L", "1L", "2L"],
            "NodeTypes" : [ "stoplight", "priority" ]
	},

	{
	    "Name" : "Intersection 3way 4lane by 4lane",
	    "AssetID" : "5a629990-da65-4f00-bb38-afa0a359d462",
	    "ZOffset" : 20.5,
	    "Padding" : 15,
	    "Signature" : ["0L", "2L", "2L", "2L"],
            "NodeTypes" : [ "stoplight", "priority" ]
	},

	{
	    "Name" : "Intersection 4way 4lane by 2lane",
	    "AssetID" : "ca60b2d0-21db-458f-89be-92222b3e09a0",
	    "ZOffset" : 20.5,
	    "Padding" : 15,
	    "Signature" : ["1L", "2L", "1L", "2L"],
            "NodeTypes" : [ "stoplight", "priority" ]
	},

	{
	    "Name" : "Intersection 4way 4lane by 4lane",
	    "AssetID" : "226ae7d4-7e9d-48f8-8d3a-e05dd02c7e41",
	    "ZOffset" : 20.5,
	    "Padding" : 15,
	    "Signature" : ["2L", "2L", "2L", "2L"],
            "NodeTypes" : [ "stoplight", "priority" ]
	},

	{
	    "Name" : "Intersection 4way 2lane by 2lane",
	    "AssetID" : "b7d436cb-6674-4936-b97a-cfa89bea8e37",
	    "ZOffset" : 20.5,
	    "Padding" : 15,
	    "Signature" : ["1L", "1L", "1L", "1L"],
            "NodeTypes" : [ "stoplight", "priority" ]
	},
	    
	{
	    "Name" : "Intersection 3way 4lane by 2x2lane",
	    "AssetID" : "fc4477b6-27dd-45d1-8815-31ed704f112d",
	    "ZOffset" : 20.5,
	    "Padding" : 15,
	    "Signature" : ["1L", "0L", "1L", "2L"],
            "NodeTypes" : [ "stoplight", "priority" ]
	},
	
	{
	    "Name" : "Intersection 4way 4lane by 3x2lane",
	    "AssetID" : "48399e53-4331-4e21-9812-4e57232d1efc",
	    "ZOffset" : 20.5,
	    "Padding" : 15,
	    "Signature" : ["1L", "1L", "1L", "2L"],
            "NodeTypes" : [ "stoplight", "priority" ]
	},

	{
	    "Name" : "Intersection corner 2lane by 2lane",
	    "AssetID" : "b5f2d609-766d-41db-bcdf-412f572d6c3d",
	    "ZOffset" : 20.5,
	    "Padding" : 15,
	    "Signature" : ["0L", "0L", "1L", "1L"],
            "NodeTypes" : [ "stoplight", "priority" ]
	},

	{
	    "Name" : "Intersection corner 4lane by 4lane",
	    "AssetID" : "2650ad8b-c771-49ed-bc36-76cce2971420",
	    "ZOffset" : 20.5,
	    "Padding" : 15,
	    "Signature" : ["0L", "0L", "2L", "2L"],
            "NodeTypes" : [ "stoplight", "priority" ]
	},

	{
	    "Name" : "Residential Row 1way 1lane",
            "AssetID" : "afdcc4a3-0b7f-4e2f-baff-cd787b3508e8",
	    "ZOffset" : 25.0,
	    "Padding" : 0,
	    "Signature" : ["0L", "0L", "D", "0L"],
            "NodeTypes" : [ "residence" ]
	},

	{
	    "Name" : "Residential 1way 1lane",
            "AssetID" : "d60e8dda-620f-4b7e-86e7-51db7a8b5e47",
	    "ZOffset" : 25.4,
	    "Padding" : 0,
	    "Signature" : ["0L", "0L", "D", "0L"],
            "NodeTypes" : [ ],
            "xNodeTypes" : [ "residence" ]
	},

        {
            "Name" : "Business Box [D 0L 0L 0L]",
            "AssetID" : "1c5fcc2c-256c-4bd4-a39a-acea1afbc592",
            "ZOffset" : 26.0,
            "Padding" : 0,
            "Signature" : ["D", "0L", "0L", "0L"],
            "NodeTypes" : ["business"]
        },

	{
	    "Name" : "Intersection 2Lane Driveway",
	    "AssetID" : "696c39eb-fbb4-4273-b860-bc3b6db35053",
	    "ZOffset" : 20.5,
	    "Padding" : 2.5,
	    "Signature" : ["1L", "D", "1L", "D"],
            "NodeTypes" : [ "driveway" ]
	},

	{
	    "Name" : "Intersection 2Lane Driveway",
	    "AssetID" : "696c39eb-fbb4-4273-b860-bc3b6db35053",
	    "ZOffset" : 20.5,
	    "Padding" : 2.5,
	    "Signature" : ["1L", "0L", "1L", "D"],
            "NodeTypes" : [ "driveway" ]
	},

	{
	    "Name" : "Intersection 2Lane Driveway",
	    "AssetID" : "696c39eb-fbb4-4273-b860-bc3b6db35053",
	    "ZOffset" : 20.5,
	    "Padding" : 2.5,
	    "Signature" : ["1L", "0L", "1L", "0L"],
            "NodeTypes" : [ "driveway" ]
	},

	{
	    "Name" : "Intersection 2Lane Driveway",
	    "AssetID" : "696c39eb-fbb4-4273-b860-bc3b6db35053",
	    "ZOffset" : 20.5,
	    "Padding" : 2.5,
	    "Signature" : ["1L", "0L", "0L", "1L"],
            "NodeTypes" : [ "driveway" ]
	},

	{
	    "Name" : "Intersection 2Lane Driveway",
	    "AssetID" : "696c39eb-fbb4-4273-b860-bc3b6db35053",
	    "ZOffset" : 20.5,
	    "Padding" : 2.5,
	    "Signature" : ["1L", "1L", "0L", "1L"],
            "NodeTypes" : [ "driveway" ]
	},

	{
	    "Name" : "Intersection 4Lane Driveway",
	    "AssetID" : "620272dc-4613-4a43-94d5-889628280c69",
	    "ZOffset" : 20.5,
	    "Padding" : 5,
	    "Signature" : ["2L", "D", "2L", "D"],
            "NodeTypes" : [ "driveway" ]
	}
    ],

    "VehicleTypes" :
    [
        {
            "Name" : "BlueCar",
            "Description" : "A blue car",
            "Rate" : 15,
	    "SourceNodeTypes" : ["residence", "business"],
	    "DestinationNodeTypes" : ["residence", "business"],
	    "Acceleration" : 0.3,
	    "Deceleration" : 0.3,
	    "Sigma" : 0.5,
	    "Length" : 3,
	    "MinGap" : 2,
	    "MaxSpeed" : 2.0,
            "AssetID" : "ed734b7e-7496-49aa-acfa-3ac84abababa",
            "StartParam" : "{ 'color' : '<0.0, 0.0, 1.0>', 'scale' : '<0.5, 2.0, 0.5>' }",
            "Position" : [128.0, 128.0, 30.0],
            "Rotation" : [0.0, 0.0, 0.0, 1.0],
            "Velocity" : [0.0, 0.0, 0.0],
            "StartParameter" : "{}"
        },

        {
            "Name" : "OrangeCar",
            "Description" : "A red car",
            "Rate" : 15,
	    "SourceNodeTypes" : ["residence", "business"],
	    "DestinationNodeTypes" : ["residence", "business"],
	    "Acceleration" : 0.8,
	    "Deceleration" : 0.8,
	    "Sigma" : 0.5,
	    "Length" : 2,
	    "MinGap" : 2,
	    "MaxSpeed" : 4.0,
            "AssetID" : "ed734b7e-7496-49aa-acfa-3ac84abababa",
            "StartParam" : "{ 'color' : '<1.0, 0.5, 0.0>', 'scale' : '<0.5, 2.0, 0.5>' }",
            "Position" : [128.0, 128.0, 30.0],
            "Rotation" : [0.0, 0.0, 0.0, 1.0],
            "Velocity" : [0.0, 0.0, 0.0],
            "StartParameter" : "{}"
        },
        
        {
            "Name" : "PurpleCar",
            "Description" : "A red car",
            "Rate" : 15,
	    "SourceNodeTypes" : ["residence", "business"],
	    "DestinationNodeTypes" : ["residence", "business"],
	    "Acceleration" : 0.2,
	    "Deceleration" : 0.2,
	    "Sigma" : 0.5,
	    "Length" : 2,
	    "MinGap" : 2,
	    "MaxSpeed" : 1.2,
            "AssetID" : "ed734b7e-7496-49aa-acfa-3ac84abababa",
            "StartParam" : "{ 'color' : '<1.0, 0.0, 1.0>', 'scale' : '<0.5, 2.0, 0.5>' }",
            "Position" : [128.0, 128.0, 30.0],
            "Rotation" : [0.0, 0.0, 0.0, 1.0],
            "Velocity" : [0.0, 0.0, 0.0],
            "StartParameter" : "{}"
        },
        
        {
            "Name" : "RedCar",
            "Description" : "A red car",
            "Rate" : 15,
	    "SourceNodeTypes" : ["residence", "business"],
	    "DestinationNodeTypes" : ["residence", "business"],
	    "Acceleration" : 0.4,
	    "Deceleration" : 0.4,
	    "Sigma" : 0.5,
	    "Length" : 3,
	    "MinGap" : 2,
	    "MaxSpeed" : 3.0,
            "AssetID" : "ed734b7e-7496-49aa-acfa-3ac84abababa",
            "StartParam" : "{ 'color' : '<1.0, 0.0, 0.0>', 'scale' : '<0.5, 2.0, 0.5>' }",
            "Position" : [128.0, 128.0, 30.0],
            "Rotation" : [0.0, 0.0, 0.0, 1.0],
            "Velocity" : [0.0, 0.0, 0.0],
            "StartParameter" : "{}"
        },

        {
            "Name" : "Train",
            "Description" : "A one car train",
            "Rate" : 0,
	    "SourceNodeTypes" : ["station"],
	    "DestinationNodeTypes" : ["station"],
	    "Acceleration" : 0.1,
	    "Deceleration" : 0.1,
	    "Sigma" : 0.1,
	    "Length" : 8,
	    "MinGap" : 1,
	    "MaxSpeed" : 3.0,
	    "AssetID" : "d8f32d8f-bd4e-4ed7-ba17-3a1420c332e2",
            "OldAssetID" : "3c053732-8f49-4613-8ed2-a6775940864b",
            "Position" : [128.0, 128.0, 30.0],
            "Rotation" : [0.0, 0.0, 0.0, 1.0],
            "Velocity" : [0.0, 0.0, 0.0],
            "StartParameter" : "{}"
        },

        {
            "Name" : "Van",
            "Description" : "A green van",
            "Rate" : 5,
	    "SourceNodeTypes" : ["residence", "business"],
	    "DestinationNodeTypes" : ["residence", "business"],
	    "Acceleration" : 0.2,
	    "Deceleration" : 0.2,
	    "Sigma" : 0.5,
	    "Length" : 4,
	    "MinGap" : 2,
	    "MaxSpeed" : 1.0,
            "AssetID" : "51505cf3-1903-41cd-acb2-c684ec6426a6",
            "Position" : [128.0, 128.0, 30.0],
            "Rotation" : [0.0, 0.0, 0.0, 1.0],
            "Velocity" : [0.0, 0.0, 0.0],
            "StartParameter" : "{}"
        }
    ]
}
