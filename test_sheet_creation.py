from spreadsheet_service import add_job_to_sheet

test_job_data = {
    'date_applied' : '2024-11-14',
    'company':'Amazon',
    'status':'Applied'
}

add_job_to_sheet(test_job_data)
print("Sheet created and row added succesfullty ")