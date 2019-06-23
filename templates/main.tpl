% rebase('templates/base.tpl', title='Queue')
<div style="padding-left:20px">
	<h4 style="display:inline-block">Currently Playing: {{current[1]}}</h4>
	<a href="/skip"><i class="material-icons">skip_next</i></a>
	<br />
	%if volume > 0:
	<a href="/volume/{{volume-10}}"><i class="material-icons">remove</i></a>
	%end
	Volume: {{volume}}%
	%if volume < 130:
	<a href="/volume/{{volume+10}}"><i class="material-icons">add</i></a>
	%end
</div>
<ul class="collection with-header" style="border-color: transparent">
	<li class="collection-header grey darken-4" style="border-bottom-color: transparent">
		<h4>Queue ({{numVids}} Songs)</h4>
	</li>
	%for vid in videos:
		<li class="collection-item grey darken-4" style="border-bottom-color: transparent"><div>
			<img src="https://img.youtube.com/vi/{{vid[0]}}/default.jpg" style="display: inline-block; vertical-align: text-top">
			<span>{{vid[1]}}</span>
			<a href="/remove/{{vid[0]}}" class="secondary-content"><i class="material-icons">remove_circle</i></a>
			<a href="/rec/{{vid[0]}}/{{vid[2]}}" class="secondary-content"><i class="material-icons">more_horiz</i></a>
		</div></li>
	%end
</ul>
