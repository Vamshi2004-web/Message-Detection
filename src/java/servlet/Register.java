/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package servlet;

import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.sql.*;
import javax.servlet.RequestDispatcher;

/**
 *
 * @author DELL
 */
public class Register extends HttpServlet {

    /**
     * Processes requests for both HTTP <code>GET</code> and <code>POST</code>
     * methods.
     *
     * @param request servlet request
     * @param response servlet response
     * @throws ServletException if a servlet-specific error occurs
     * @throws IOException if an I/O error occurs
     */
    protected void processRequest(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        response.setContentType("text/html;charset=UTF-8");
        try (PrintWriter out = response.getWriter()) {
            /* TODO output your page here. You may use following sample code. */
            out.println("<!DOCTYPE html>");
            out.println("<html>");
            out.println("<head>");
            out.println("<title>Servlet Register</title>");            
            out.println("</head>");
            out.println("<body>");
            out.println("<h1>Servlet Register at " + request.getContextPath() + "</h1>");
            out.println("</body>");
            out.println("</html>");
        }
    }

    // <editor-fold defaultstate="collapsed" desc="HttpServlet methods. Click on the + sign on the left to edit the code.">
    /**
     * Handles the HTTP <code>GET</code> method.
     *
     * @param request servlet request
     * @param response servlet response
     * @throws ServletException if a servlet-specific error occurs
     * @throws IOException if an I/O error occurs
     */
    @Override
protected void doGet(HttpServletRequest request, HttpServletResponse response)
        throws ServletException, IOException {
        PrintWriter out = response.getWriter();
        Connection con = null;
        PreparedStatement pstmt = null;
        String n = "", p = "", x = "", y = "";
        
        // Get parameters from the request
        n = request.getParameter("username");
        x = request.getParameter("email");
        p = request.getParameter("password");
        y = request.getParameter("confirmpassword");
        
        try {
            
            Class.forName("org.apache.derby.jdbc.ClientDriver");
            
            
            con = DriverManager.getConnection("jdbc:derby://localhost:1527/user", "root", "root");
            
            
            String sql = "INSERT INTO root.registerspam(username, email, password, confirmpassword) VALUES (?, ?, ?, ?)";
            pstmt = con.prepareStatement(sql);
            pstmt.setString(1, n);
            pstmt.setString(2, x);
            pstmt.setString(3, p);
            pstmt.setString(4, y);
            
            
            pstmt.executeUpdate();
            
            
            RequestDispatcher rd = request.getRequestDispatcher("index_1.html");
            rd.forward(request, response);
        } catch (Exception e) {
            out.print(e);
            out.println("<font color=red size=24>Register failed!!<br>");
            out.println("<a href=registration.html>Go back</a>");
        } finally {
            try {
                
                if (pstmt != null) {
                    pstmt.close();
                }
                if (con != null) {
                    con.close();
                }
                if (out != null) {
                    out.close();
                }
            } catch (SQLException ex) {
                out.println("Error in closing resources: " + ex.getMessage());
            }
        }
    }


    /**
     * Handles the HTTP <code>POST</code> method.
     *
     * @param request servlet request
     * @param response servlet response
     * @throws ServletException if a servlet-specific error occurs
     * @throws IOException if an I/O error occurs
     */
    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        processRequest(request, response);
    }

    /**
     * Returns a short description of the servlet.
     *
     * @return a String containing servlet description
     */
    @Override
    public String getServletInfo() {
        return "Short description";
    }// </editor-fold>

}
