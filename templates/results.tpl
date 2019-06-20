% rebase('templates/base.tpl', title='Results')
<div style="margin-left: 20px">
	<h4>{{header}}</h4>
	{{subheader}}
</div>
<ul class="collection" style="border-color: transparent">
	%for vid in videos:
		<li onclick="M.toast({html: 'Added to Queue.<button class=\'btn-flat toast-action\'>Undo</button>'})"
		        class="collection-item grey darken-4" style="border-bottom-color: transparent"><div>
			<!-- a href="/add/{{vid[0]}}/{{vid[2]}}">ADD</a-->
			<img src="https://img.youtube.com/vi/{{vid[0]}}/default.jpg">
			<span>{{vid[1]}}</span>
			<a href="/rec/{{vid[0]}}/{{vid[2]}}" class="secondary-content">
				<i class="material-icons">more_horiz</i>
			</a>
		</div></li>
	%end
</ul>
