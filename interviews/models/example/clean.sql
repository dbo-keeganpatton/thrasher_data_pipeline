/*
	Remove Punctuation and lone 's' instances.
*/
{{ config(materialized='table') }}


with
	remove_punctuation as(
		select 
			regexp_replace(title, '[[:punct:]]', ' ', 'g') as title,
			regexp_replace(question, '[[:punct:]]', ' ', 'g') as question,
			regexp_replace(answer, '[[:punct:]]', ' ', 'g') as answer
		from {{ ref('lower') }}	
	),

	drop_single_s as(
		select
			regexp_replace(title, '\ s ', '', 'g') as title,
			regexp_replace(question, '\ s ', '', 'g') as question,
			regexp_replace(answer, '\ s ', '', 'g') as answer
		from remove_punctuation
	)


select * from drop_single_s

