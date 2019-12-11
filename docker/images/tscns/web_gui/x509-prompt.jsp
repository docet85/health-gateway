<%@ taglib uri="http://www.springframework.org/tags" prefix="spring" %>
<%@ taglib uri="urn:mace:shibboleth:2.0:idp:ui" prefix="idpui" %>
<%@ page import="javax.servlet.http.Cookie" %>
<%@ page import="org.opensaml.profile.context.ProfileRequestContext" %>
<%@ page import="net.shibboleth.idp.authn.ExternalAuthentication" %>
<%@ page import="net.shibboleth.idp.authn.context.AuthenticationContext" %>
<%@ page import="net.shibboleth.idp.profile.context.RelyingPartyContext" %>
<%@ page import="net.shibboleth.idp.ui.context.RelyingPartyUIContext" %>

<%
response.sendRedirect(request.getContextPath() + "/Authn/X509?"
    + ExternalAuthentication.CONVERSATION_KEY + "="
    + request.getParameter(ExternalAuthentication.CONVERSATION_KEY));

//request.setAttribute("javax.servlet.request.X509Certificate", null);
final String key = ExternalAuthentication.startExternalAuthentication(request);
final ProfileRequestContext prc = ExternalAuthentication.getProfileRequestContext(key, request);
final AuthenticationContext authnContext = prc.getSubcontext(AuthenticationContext.class);
final RelyingPartyContext rpContext = prc.getSubcontext(RelyingPartyContext.class);
final RelyingPartyUIContext rpUIContext = authnContext.getSubcontext(RelyingPartyUIContext.class);
final boolean identifiedRP = rpUIContext != null && !rpContext.getRelyingPartyId().contains(rpUIContext.getServiceName());
%>

<!DOCTYPE html>
<html>

<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
  <title>
    <spring:message code="idp.title" text="Web Login Service" />
  </title>
  <link rel="stylesheet" type="text/css" href="<%= request.getContextPath()%>/css/bootstrap.css">
</head>

<body>
</body>

</html>