/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package servlet;

import java.io.IOException;
import java.io.PrintWriter;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import javax.servlet.RequestDispatcher;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

/**
 *
 * @author DELL
 */
public class login extends HttpServlet {

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
            out.println("<title>Servlet login</title>");            
            out.println("</head>");
            out.println("<body>");
            out.println("<h1>Servlet login at " + request.getContextPath() + "</h1>");
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
        processRequest(request, response);
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
        PrintWriter out = response.getWriter();
        Connection con = null;
        PreparedStatement pstmt = null;
        String n = "", p = "";

        // Get parameters from the request
        n = request.getParameter("username");
        p = request.getParameter("password");

        try {
            // Load the Apache Derby JDBC driver
            Class.forName("org.apache.derby.jdbc.ClientDriver");

            // Establish connection to the Derby database (adjust URL if needed)
            con = DriverManager.getConnection("jdbc:derby://localhost:1527/user","root", "root");

            // Prepare the SQL query for login verification
            String sql = "SELECT username FROM root.registerspam WHERE username=? AND password=?";
            pstmt = con.prepareStatement(sql);
            pstmt.setString(1, n);
            pstmt.setString(2, p);

            // Execute the query
            ResultSet rs = pstmt.executeQuery();

            if (rs.next()) {
                // If the username and password match, forward to the dashboard
                RequestDispatcher rd = request.getRequestDispatcher("dashboard.html");
                rd.forward(request, response);
            } else {
                // If login fails, show an error message
                out.println("<font color=red size=24>Login failed! Invalid username or password.<br>");
                out.println("<a href='index_1.html'>Go back to login</a>");
            }
        } catch (Exception e) {
            // Catch and display any error
            out.println("<font color=red size=24>Error: " + e.getMessage() + "<br>");
        } finally {
            try {
                // Close resources
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
     * Returns a short description of the servlet.
     *
     * @return a String containing servlet description
     */
    @Override
    public String getServletInfo() {
        return "Short description";
    }// </editor-fold>

}
