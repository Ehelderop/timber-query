# timber-query
A tool to query parcels in WA counties for logging suitability

README for Timber parcel filter and parcel CSV editor

Update April 27, 2020: San Juan County has been added but has incomplete owner info in its dataset. As such, some of those filters may not work correctly when filtering the parcels. However, if parcels are filtered based on other criteria, that owner info can be found when accessing the San Juan County assessor website using the CSV Edit program.

**Parcel Filter**

Within the Parcel filter folder you will see Inputs, Outputs, TimberGUI, and timberGui_newCounties.exe. The contents of the Inputs and TimberGUI folders should not be moved or changed at all. Use the .exe to start the program. The outputs folder is currently empty, it is there as a placeholder. Feel free to save outputs to other places on your computer.

Within the Parcel filter program, select one of the county folders within the provided Inputs folder as the Input File Directory. Select any location for the output files to be saved to.
 ![alt text](https://github.com/Ehelderop/timber-query/blob/master/imgs/Parcel_img1.png)

Select one of the three owner status radio buttons. The private owner only filters out government entities, corporations, religious organizations, native american tribes, etc. as owners.

Note that ownership info is missing for Clallam and Jefferson parcels – these radio buttons will not work to filter those counties based on owner data.

And note that Island and San Juan county are missing their parcel use codes, so the private owner only button will not work for those counties.

Road parcel access checks for parcels within a kilometer of an existing road, while the water feature checkmark excludes parcels that have water features.

The size filter sets a minimum acreage for parcels (parcels smaller than the size you enter will be filtered out).

Land to total value ratio ranges from 0 to 1 and is a ratio of the total market value to the total land value.

The percent coverage fields take a value from 0 to 100 and remove any parcels that have coverages lower than what you specify.

Run with selected filters to generate the output CSV in the selected output folder (this can take up to a minute).


**CSV Editor**

Once again, leave the contents of these subfolders intact. Use the CSVEdit_newCounties.exe to start the program.

NOTE: The first time you run this, it may trigger your computer’s antivirus/firewall – this is because the program automatically interfaces with your browser, which may be detected as a threat. Give the .exe the permissions it needs, and you may need to close the program and start it again after doing so.

As before, select the input CSV file that you wish to use (this should be one of two files: either one generated by the Parcel filter program OR one generated by this program when you save your edits).
![alt text](https://github.com/Ehelderop/timber-query/blob/master/imgs/CSV_img1.png) 

Select an output folder where you would like to save your notes. This can be the same as the output folder from the Parcel filter program, but it does not have to be.

When you have selected your CSV file, load it by clicking the Load selected CSV button. You will see several fields automatically populate. Any fields that automatically populate cannot be edited, they are there for display purposes for the user’s reference only.

Note that due to missing owner/taxpayer info in some county datasets, some of these fields will display that they are missing data. In these cases, the owner info can be seen by the user in the web browser after clicking the Open parcel page button.

Navigate between parcels by clicking the Next parcel and Previous parcel buttons. Any notes you have taken in the four note fields (Clay’s timber rank, Clay’s complete rank, General notes, and Contact notes) are saved while you navigate.

Clicking the Open parcel page button will load the current parcel’s webpage in the browser window. This can take several seconds. Feel free to explore whatever info you need in the browser window, when you next click Open parcel page, it will reset (just don’t close the browser window entirely).

Finally, click Save and quit to save your notes. You can revisit the notes you have made by opening the resulting CSV in this program again – it will pick up where you left off. These CSVs can also be opened in Excel. However, if they are edited too much in Excel they will not be able to be opened in this program anymore.
