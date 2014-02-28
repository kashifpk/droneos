<%inherit file="pyckauth_base.mako"/>


<div>
<h1>droneos_ui - Authentication Manager - Users</h1>

%if "edit"==action:
<form action="${request.current_route_url()}?action=edit&id=${user.user_id}" method="post">
%else:
<form action="${request.current_route_url()}" method="post">
%endif

<table style="margin: auto;">
    ${user_form.as_table() | n}
    
    <tr>
        <td>
            <table>
                <tr class="tr_heading">
                    <th>Permissions</th>
                </tr>
                <tr>
                    <td>
                        %for P in permissions:
                            %if 'add' == action:
                            <input type="checkbox" name="chk_perm_${P.permission}" value="${P.permission}" /> ${P.permission} &nbsp;&nbsp
                            %else:
                                <% checked='' %>
                                %for up in user.permissions:
                                    %if up.permission == P.permission:
                                        <% checked='checked="true"' %>
                                    %endif
                                %endfor
                                <input type="checkbox" name="chk_perm_${P.permission}" value="${P.permission}" ${checked} /> ${P.permission} &nbsp;&nbsp
                            %endif
                            
                            %if 0!=loop.index and 0==loop.index%8:
                            <br />
                            %endif
                        %endfor
                        
                    </td>
                </tr>
            </table>
        </td>
    </tr>
    
    <tr>
        <td style="text-align: right">
            <input type="submit" value="${action.title()} User" class="button green" />
        </td>
    </tr>
</table>
</form>

<br /><br />

<table style="margin: auto;">
    <tr class="tr_heading">
        <th>User ID</th>
        <th>Permissions</th>
        <th></th>   
    </tr>
    
    %for U in users:
    
    <tr class="${loop.cycle('oddrow', 'evenrow')}">
        <td>${U.user_id}</td>
        <td>
            %for P in U.permissions:
            <span style="padding: 1px 6px; background-color: #A6DDA7;">${P.permission}</span>
            %if 0!=loop.index and 0==loop.index%8:
            <br />
            %endif
            %endfor
        </td>
        <td>
            <a href="${request.current_route_url()}?action=edit&id=${U.user_id}">Edit</a>
            <a href="${request.current_route_url()}?action=delete&id=${U.user_id}">Delete</a> 
        </td>
    </tr>
    
    %endfor
</table>


</div>

