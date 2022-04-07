from flee import flee
from flee.datamanager import handle_refugee_data, read_period
from flee import InputGeography
import numpy as np
import flee.postprocessing.analysis as a
import sys
import os
import random

def AddInitialRefugees(e,d,loc):
    """
    Add the initial refugees to a location, using the location name
    """
    num_refugees = int(d.get_field(name=loc.name, day=0, FullInterpolation=True))
    for _ in range(0, num_refugees):
        e.addAgent(location=loc)


insert_day0_refugees_in_camps = True

if __name__ == "__main__":

    #end_time = read_period.read_conflict_period(fname=os.path.join(sys.argv[1],"conflict_period.csv"))
    #last_physical_day = 10
    max_windspeed = 150
    current_windspeed = 0
    end_time = 15
    last_physical_day = 15

    if len(sys.argv) < 5:
        print(
            "Please run using: python3 run.py <your_csv_directory> "
            "<your_refugee_data_directory> <duration in days> <starting windspeed> <maximum windspeed>"
            "<optional: simulation_settings.csv> > <output_directory>/<output_csv_filename>"
        )

    input_csv_directory = sys.argv[1]
    validation_data_directory = sys.argv[2]
    if int(sys.argv[3]) > 0:
        end_time = int(sys.argv[3])
        last_physical_day = end_time

    if int(sys.argv[4]) > 0:
        current_windspeed = int(sys.argv[4])
        flee.Ecosystem.windspeed = current_windspeed

    if int(sys.argv[5]) > 0:
        max_windspeed = int(sys.argv[5])

    if len(sys.argv) == 7:
        flee.SimulationSettings.ReadFromCSV(sys.argv[6])

    flee.SimulationSettings.FlareConflictInputFile = os.path.join(
        input_csv_directory, "conflicts.csv"
    )

    e = flee.Ecosystem()

    ig = InputGeography.InputGeography()

    ig.ReadFlareConflictInputCSV(csv_name=flee.SimulationSettings.FlareConflictInputFile)

    ig.ReadLocationsFromCSV(csv_name=os.path.join(input_csv_directory, "locations.csv"))

    ig.ReadLinksFromCSV(csv_name=os.path.join(input_csv_directory, "routes.csv"))

    ig.ReadClosuresFromCSV(csv_name=os.path.join(input_csv_directory, "closures.csv"))

    e, lm = ig.StoreInputGeographyInEcosystem(e)

    d = handle_refugee_data.RefugeeTable( csvformat="generic", data_directory="flee/config_template/source_data/",start_date="2015-03-04",data_layout="data_layout.csv")

    output_header_string = "Day,"

    camp_locations = e.get_camp_names()

    #lm["Port Vila Central Hospital"].capacity = d.getMaxFromData("Port Vila Central Hospital",last_physical_day)
    #lm["National Museum Vanuatu"].capacity = d.getMaxFromData("National Museum Vanuatu",last_physical_day)

    for camp_name in camp_locations:
        if insert_day0_refugees_in_camps:
            AddInitialRefugees(e, d, lm[camp_name])
        output_header_string += "{} sim,{} data,{} error,".format(
            lm[camp_name].name, lm[camp_name].name, lm[camp_name].name
        )

    output_header_string += (
        "Total error,refugees in camps (UNHCR),total residents (simulation),"
        "raw UNHCR refugee count,residents in shelters (simulation),refugee_debt"
    )

    print(output_header_string)

    # Set up a mechanism to incorporate temporary decreases in refugees
    refugee_debt = 0
    refugees_raw = 0  # raw (interpolated) data from TOTAL UNHCR refugee count only.

    #Increasing windspeed rapidly at the start of the simulation 
    #And decreasing after maximum windspeed has reached or quarter of the duration has passed
    for t in range(0, end_time):

        if (t < end_time/4):
            if(flee.Ecosystem.windspeed < max_windspeed):
                flee.Ecosystem.windspeed += random.choice([15,20,35])
                #print(f"if: {flee.Ecosystem.windspeed}")
        else:
                flee.Ecosystem.windspeed -= random.choice([10,5,15])
            #print(f"Else: {flee.Ecosystem.windspeed}")
        # if t>0:
        ig.AddNewConflictZones(e=e, time=t)

        # Determine number of new refugees to insert into the system.
        new_refs = d.get_daily_difference(day=t, FullInterpolation=True) - refugee_debt
        refugees_raw += d.get_daily_difference(day=t, FullInterpolation=True)

        # Refugees are pre-placed in Mali, so set new_refs to 0 on Day 0.
        if insert_day0_refugees_in_camps:
            if t == 0:
                new_refs = 0
                # refugees_raw = 0

        if new_refs < 0:
            refugee_debt = -new_refs
            new_refs = 0
        elif refugee_debt > 0:
            refugee_debt = 0

        # Insert refugee agents
        for _ in range(0, new_refs):
            e.addAgent(location=e.pick_conflict_location())

        e.refresh_conflict_weights()
        t_data = t

        e.enact_border_closures(time=t)
        e.evolve()

        # Calculation of error terms
        errors = []
        abs_errors = []
        loc_data = []

        camps = []
        for camp_name in camp_locations:
            camps += [lm[camp_name]]
            loc_data += [d.get_field(name=camp_name, day=t)]

        # calculate retrofitted time.
        refugees_in_camps_sim = 0
        for c in camps:
            refugees_in_camps_sim += c.numAgents

        # calculate errors
        j = 0
        for i in camp_locations:
            errors += [a.rel_error(val=lm[i].numAgents, correct_val=loc_data[j])]
            abs_errors += [a.abs_error(val=lm[i].numAgents, correct_val=loc_data[j])]

            j += 1

        output = "%s" % t

        for i in range(0, len(errors)):
            output += ",{},{},{}".format(lm[camp_locations[i]].numAgents, loc_data[i], errors[i])

        if refugees_raw > 0:
            output += ",{},{},{},{},{},{}" .format(
                float(np.sum(abs_errors)) / float(refugees_raw),
                int(sum(loc_data)),
                e.numAgents(),
                refugees_raw,
                refugees_in_camps_sim,
                refugee_debt
            )
        else:
            output += ",0,0,0,0,0,0"

        print(output)
