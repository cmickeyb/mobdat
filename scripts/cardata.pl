#!/usr/bin/perl

use JSON;
use Text::CSV;

my $scale = 0.6;

my @cars = ();
my @header = ();

my $parser = Text::CSV->new({ sep_char => ',' });

while (<>) 
{
    trim;
    die "Unable to parse header line; $_\n" unless $parser->parse($_);
    @header = $parser->fields();
    last;
}

my $json = JSON->new->pretty->allow_nonref;
my $data = {};

while (<>) 
{
    trim;
    continue unless $parser->parse($_);

    my @cardata = $parser->fields();
    my %car = {};
    for (my $i = 0; $i <= $#header; $i++)
    {
        $car{$header[$i]} = $cardata[$i];
    }

    $data = {};

    $data->{'Name'} = sprintf("%s %s", $car{'Name'}, $car{'Color'});
    $data->{'Description'} = $car{'Description'};
    @profiles = split(/, */, $car{'ProfileTypes'});
    $data->{'ProfileTypes'} = \@profiles;
    $data->{'Rate'} = $car{'Rate'} + 0;
    $data->{'Acceleration'} = $car{'Acceleration'} + 0.0;
    $data->{'Deceleration'} = $car{'Deceleration'} + 0.0;
    $data->{'Sigma'} = $car{'Sigma'} + 0.0;
    $data->{'Length'} = $car{'Length'} + 0.0;
    $data->{'MinGap'} = $car{'MinGap'} + 0.0;
    $data->{'MaxSpeed'} = $car{'MaxSpeed'} + 0.0;
    $data->{'AssetID'} = {};
    $data->{'AssetID'}{'ObjectName'} = $car{'Name'};
    $data->{'AssetID'}{'ItemName'} = $data->{'Name'};
    $data->{'StartParameter'} = "{ 'terminate' : 1, 'scale' : $scale }";

    push(@cars, $data);
}

print $json->encode({'VehicleTypes' => \@cars});

