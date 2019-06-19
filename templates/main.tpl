% rebase('templates/base.tpl', title='Queue')
<div style="padding-left:20px">
	<h4 style="display:inline-block">Currently Playing: {{current[1]}}
	</h4><br />
	Volume: {{volume}}%
</div>
<ul class="collection with-header">
	<li class="collection-header"><h4>Queue ({{numVids}} Songs)</h4></li>
	%for vid in videos:
		<li class="collection-item"><div>
			<img src="https://img.youtube.com/vi/{{vid[0]}}/default.jpg">
			<span class="title">{{vid[1]}}</span>
			<a href="/remove/{{vid[0]}}" class="secondary-content"><i class="material-icons">remove_circle</i></a>
			<a href="/rec/{{vid[0]}}/{{vid[2]}}" class="secondary-content"><i class="material-icons">more_horiz</i></a>
		</div></li>
	%end
</ul>
