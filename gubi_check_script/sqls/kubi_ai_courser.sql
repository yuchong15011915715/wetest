USE pjx;
SELECT id, `code`, `name`, course_picture_url AS img1,standard_img_url AS img2, ai_course_url AS html, 
	static_resource_url AS zip1, media_resource_url AS zip2, video_url AS video
FROM course
;