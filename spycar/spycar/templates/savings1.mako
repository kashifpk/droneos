<%inherit file="base.mako"/>
<h2><u> Paths table </u></h2>
<table>
<tr>
<th width="70">&nbsp;PATH ID</th>
<th width="300">NAME </th>
<th width="300">DESCRIPTION </th>
</tr>
</table>





%for category in acc2:
<table border="3">
<tr>
<td width="70">
<h3>&nbsp;&nbsp;&nbsp;${category.id}</h3>
</td>

<td width="300">
<h3>&nbsp;&nbsp;&nbsp;${category.name}</h3>
</td>

<td width="300">
<h3>&nbsp;&nbsp;&nbsp;${category.desc}</h3>
</td>


</tr>
</table>
</div>


%endfor 
