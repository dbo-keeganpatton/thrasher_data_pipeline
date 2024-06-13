{{ config(materialized='table') }}


with
	low as(
		select 
			lower(title) as title,
			lower(question) as question,
			lower(answer) as answer  
		from interviews i 
	)

select * from low
	

